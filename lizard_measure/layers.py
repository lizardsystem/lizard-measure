import mapnik
import pkg_resources
from matplotlib.dates import date2num
from matplotlib.lines import Line2D
import datetime

from lizard_map import adapter
from lizard_map import coordinates
from lizard_map import workspace
from lizard_map.utility import short_string

from lizard_shape.models import Shape

from lizard_krw.models import SCORE_CATEGORY_FYTO
from lizard_krw.models import SCORE_CATEGORY_FLORA
from lizard_krw.models import SCORE_CATEGORY_FAUNA
from lizard_krw.models import SCORE_CATEGORY_VIS
from lizard_krw.models import AlphaScore
from lizard_krw.models import Measure
from lizard_krw.models import MeasureStatus
from lizard_krw.models import Score
from lizard_krw.models import WaterBody

ICON_STYLE = {
    'measure': {
        'icon': 'shovel.png',
        'mask': ('mask.png', ),
        'color': (0, 1, 0, 0)},
    'score-fyto': {
        'icon': 'polygon.png',
        'mask': ('mask.png', ),
        'color': (0, 1, 1, 0)},
    'score-flora': {
        'icon': 'polygon.png',
        'mask': ('mask.png', ),
        'color': (1, 1, 0, 0)},
    'score-fauna': {
        'icon': 'polygon.png',
        'mask': ('mask.png', ),
        'color': (1, 0, 1, 0)},
    'score-vis': {
        'icon': 'polygon.png',
        'mask': ('mask.png', ),
        'color': (0, 0, 1, 0)},
    }


class WorkspaceItemAdapterKrw(workspace.WorkspaceItemAdapter):
    """
    Should be registered as adapter_krw

    identifier = {
      'google_x': ...,
      'google_y': ...,
      'measure_id': for layer_name=measure only,
      'waterbody_slug': ...,
      }

    if you fill in shape_id in layer_arguments, the adapter will take
    the shapefile associated with that shape.

    """

    def __init__(self, *args, **kwargs):
        super(WorkspaceItemAdapterKrw, self).__init__(*args, **kwargs)
        self.layer_name = self.layer_arguments['layer']
        # ^^^ Which layer should be displayed?
        self.layer_colors = {
            "measure": "#88ff88",
            "score-vis": "#8888ff",
            "score-fyto": "#88ffff",
            "score-flora": "#ffff88",
            "score-fauna": "#ff88ff",
            "background": "#ffb9d5"}
        if 'waterbody_slug' in self.layer_arguments:
            self.waterbody_slug = self.layer_arguments['waterbody_slug']
        else:
            self.waterbody_slug = None
        if 'shape_slug' in self.layer_arguments:
            self.shape_slug = self.layer_arguments['shape_slug']
            self.shape = Shape.objects.get(slug=self.shape_slug)
            self.shape_filename = str(self.shape.shp_file.file.name)
        else:
            # Default shape
            self.shape_filename = pkg_resources.resource_filename(
                'lizard_map',
                'test_shapefiles/KRWwaterlichamen_merge.shp')

    def layer(self, layer_ids=None, request=None):
        """Return layer and styles for a shapefile.

        """

        layers = []
        styles = {}
        layer = mapnik.Layer("Krw gegevens", coordinates.RD)
        # TODO: ^^^ translation!
        layer.datasource = mapnik.Shapefile(
            file=self.shape_filename)
        area_looks = mapnik.PolygonSymbolizer(
            mapnik.Color(self.layer_colors[self.layer_name]))
        if self.layer_name == 'background':
            line_looks = mapnik.LineSymbolizer(mapnik.Color('#dddddd'), 1)
        else:
            line_looks = mapnik.LineSymbolizer(mapnik.Color('#dd0000'), 1)

        area_looks.fill_opacity = 0.5
        layout_rule = mapnik.Rule()
        layout_rule.symbols.append(area_looks)
        layout_rule.symbols.append(line_looks)
        area_style = mapnik.Style()

        area_style.rules.append(layout_rule)

        if self.waterbody_slug:
            # light up area
            water_body = WaterBody.objects.get(slug=self.waterbody_slug)
            layout_rule_waterbody = mapnik.Rule()
            area_looks_waterbody = mapnik.PolygonSymbolizer(
                mapnik.Color("#ff0000"))
            line_looks_waterbody = mapnik.LineSymbolizer(
                mapnik.Color('#dd0000'), 1)
            layout_rule_waterbody.symbols.append(area_looks_waterbody)
            layout_rule_waterbody.symbols.append(line_looks_waterbody)
            layout_rule_waterbody.filter = mapnik.Filter(
                "[WGBNAAM] = '%s'" % str(water_body.name))
            area_style.rules.append(layout_rule_waterbody)

        styles['Area style'] = area_style
        layer.styles.append('Area style')
        layers = [layer]
        return layers, styles

    def search(self, google_x, google_y, radius=None):
        """
        Hacky at the moment as searching shapefiles is harder than
        expected. Copied from lizard_map.layers.py

        x,y are google coordinates

        result: list of dicts:
        distance, object, name, shortname, google_coords,
        workspace_item, identifier

        """

        # Set up a basic map as only map can search...
        mapnik_map = mapnik.Map(400, 400)
        mapnik_map.srs = coordinates.GOOGLE

        layers, styles = self.layer()
        for layer in layers:
            mapnik_map.layers.append(layer)
        for name in styles:
            mapnik_map.append_style(name, styles[name])
        # 0 is the first layer.
        feature_set = mapnik_map.query_point(0, google_x, google_y)

        result = []
        for feature in feature_set.features:
            name_in_shapefile = feature.properties['WGBNAAM']
            water_body = WaterBody.objects.get(name=name_in_shapefile)

            if self.layer_name == 'measure':
                # for each measure it returns an 'object'
                found_objects = Measure.objects.filter(waterbody=water_body)
            else:
                # score-fyto, score-flora, score-fauna, score-vis
                # always 1 'object'
                found_objects = [self.layer_name, ]

            for found_object in found_objects:
                identifier = {'waterbody_slug': water_body.slug,
                              'google_x': google_x,
                              'google_y': google_y}
                if self.layer_name == 'measure':
                    identifier['measure_id'] = found_object.id
                single_result = {
                    'distance': 0.0,
                    'object': found_object,
                    'name': str(found_object),
                    'shortname': '%s: %s' % (water_body.name, found_object),
                    'google_coords': (google_x, google_y),
                    'workspace_item': self.workspace_item,
                    'identifier': identifier,
                    }
                result.append(single_result)

        return result

    def values(self, identifier, start_date, end_date):
        result = []

        # Measure
        if self.layer_name == 'measure':
            measure = Measure.objects.get(pk=identifier['measure_id'])
            measure_msms = measure.measurestatusmoment_set.filter(
                datetime__gte=start_date, datetime__lte=end_date)
            for measure_msm in measure_msms:
                result.append({
                        'datetime': measure_msm.datetime,
                        'value': measure_msm.status.name,
                        'unit': '-'})
            return result

        # Scores
        layer_name_to_category = {
            'score-vis': SCORE_CATEGORY_VIS,
            'score-fyto': SCORE_CATEGORY_FYTO,
            'score-flora': SCORE_CATEGORY_FLORA,
            'score-fauna': SCORE_CATEGORY_FAUNA,
            }
        score_category = layer_name_to_category[self.layer_name]
        water_body = WaterBody.objects.get(slug=identifier['waterbody_slug'])
        scores = Score.objects.filter(
            category=score_category,
            start_date__gte=start_date,
            start_date__lte=end_date,
            waterbody=water_body)
        for score in scores:
            result.append({
                    'datetime': score.start_date,
                    'value': score.alpha_score.name,
                    'unit': '-'})

        return result

    def location(self, waterbody_slug, google_x, google_y,
                 measure_id=None, layout=None):
        """
        find location at waterbody_slug, x, y

        """
        water_body = WaterBody.objects.get(slug=waterbody_slug)
        identifier = {
            'waterbody_slug': waterbody_slug,
            'google_x': google_x,
            'google_y': google_y,
            }
        if measure_id is not None:
            identifier['measure_id'] = measure_id
        if measure_id is not None and self.layer_name == 'measure':
            display_object = Measure.objects.get(pk=measure_id)
            name = display_object.name
        else:
            display_object = None
            name = water_body.name

        return {
            'name': name,
            'shortname': name,
            'object': display_object,
            'workspace_item': self.workspace_item,
            'google_coords': (google_x, google_y),
            'identifier': identifier,
            }

    @classmethod
    def _image_measures(cls, graph, measures, start_date, end_date,
                        end_date_realized=None, add_legend=True,
                        title=None):
        """Function to draw measures

        TODO: when a single measure is drawn, sometimes the whole
        picture is stretched out

        !attn! measure statuses are aggregated from child measures

        """

        def calc_bar_colors(measure, end_date, is_planning):
            """Returns calculated bars. The bars are aggregated from
            measure_status_moments from sub measures.

            ** measure can also be a measure_collection. It uses the
               status_moment function only.
            """
            measure_bar = []
            measure_colors = []
            measure_status_moments = measure.measure_status_moments(
                end_date=end_date, is_planning=is_planning)
            for msm_index, msm in enumerate(measure_status_moments):
                # drawing enddate: "infinity" or next status moment
                if msm_index == len(measure_status_moments) - 1:
                    msm_end_date = end_date
                else:
                    msm_end_date = measure_status_moments[
                        msm_index + 1].datetime
                date_length = date2num(msm_end_date) - date2num(msm.datetime)

                measure_bar.append((date2num(msm.datetime), date_length))
                measure_colors.append(msm.status.color.html)
            return measure_bar, measure_colors

        if end_date_realized is None:
            end_date_realized = min(end_date, datetime.datetime.now().date())
        if title is None:
            title = "krw maatregel(en)"
        graph.suptitle(title)
        for index, measure in enumerate(measures):
            # realized
            measure_bar, measure_colors = calc_bar_colors(
                measure, end_date_realized, False)
            graph.axes.broken_barh(measure_bar,
                                   (-index - 0.3, 0.6),
                                   facecolors=measure_colors,
                                   edgecolors=measure_colors)
            # planning
            measure_bar_p, measure_colors_p = calc_bar_colors(
                measure, end_date, True)
            graph.axes.broken_barh(measure_bar_p,
                                   (-index - 0.45, 0.1),
                                   facecolors=measure_colors_p,
                                   edgecolors=measure_colors_p)

        # Y ticks
        yticklabels = [measure.shortname for measure in measures]
        yticklabels.reverse()
        graph.axes.set_yticks(range(int(-len(measures) + 0.5), 1))
        graph.axes.set_yticklabels(yticklabels)
        graph.axes.set_ylim(-len(measures) + 0.5, 0.5)

        # Legend
        if add_legend:
            legend_handles, legend_labels = [], []
            for measure_status in MeasureStatus.objects.all():
                legend_handles.append(
                    Line2D([], [], color=measure_status.color.html, lw=10))
                legend_labels.append(measure_status.name)
            graph.legend(legend_handles, legend_labels, ncol=3)

    @classmethod
    def _image_score(cls, graph, layer_name, waterbodies,
                     start_date, end_date):
        # add specific graphics to krw_graph
        graph.suptitle("krw score(s)")
        graph.axes.set_ylim(0, len(waterbodies))
        # we fit 50 scores in the graph
        score_width = (date2num(end_date) - date2num(start_date)) / 50

        score_categories = {
            'score-fyto': SCORE_CATEGORY_FYTO,
            'score-flora': SCORE_CATEGORY_FLORA,
            'score-fauna': SCORE_CATEGORY_FAUNA,
            'score-vis': SCORE_CATEGORY_VIS,
            }
        category = score_categories[layer_name]
        for index, waterbody in enumerate(waterbodies):
            scores = Score.objects.filter(start_date__gte=start_date,
                                          start_date__lte=end_date,
                                          waterbody=waterbody,
                                          category=category)
            score_data = []
            score_colors = []
            for score in scores:
                score_data.append((date2num(score.start_date), score_width))
                color = score.alpha_score.color.html
                score_colors.append(color)

            graph.axes.broken_barh(score_data,
                                   (index - 0.45, 1),
                                   facecolors=score_colors,
                                   edgecolors='grey')

        # Y ticks
        waterbodies_short = [
            short_string(wb.__unicode__(), 17) for wb in waterbodies]
        graph.axes.set_yticks(range(len(waterbodies)))
        graph.axes.set_yticklabels(waterbodies_short)
        graph.axes.set_ylim(-0.5, len(waterbodies) - 0.5)

        # Legend.
        legend_handles, legend_labels = [], []
        for alpha_score in AlphaScore.objects.all():
            legend_handles.append(
                Line2D([], [], color=alpha_score.color.html, lw=10))
            legend_labels.append(alpha_score.name)
        graph.legend(legend_handles, legend_labels, ncol=2)

    def image(self, identifier_list,
              start_date, end_date,
              width=None, height=None,
              layout_extra=None):
        """
        visualizes scores or measures in a graph

        identifier_list: [{'waterbody_slug': ...}, ...]
        start_end_dates: 2-tuple dates

        each row is an area
        """
        measures = []
        waterbodies = []
        for identifier in identifier_list:
            if self.layer_name == 'measure':
                # it's a measure
                measure = Measure.objects.get(pk=identifier['measure_id'])
                measures.append(measure)
            else:
                # krw score
                waterbody = WaterBody.objects.get(
                    slug=identifier['waterbody_slug'])
                waterbodies.append(waterbody)

        if width is None:
            width = 380.0
        if height is None:
            height = 170.0

        # Calculate own height, which can be smaller than given.
        #height = min((len(measures) + len(waterbodies)) * 40 + 20 +
        #             len(legend_handles) * 10.0, height)

        graph = adapter.Graph(start_date, end_date, width, height)
        if measures:
            # krw measures
            self._image_measures(graph, measures, start_date, end_date)
        else:
            # krw-score
            self._image_score(graph, self.layer_name, waterbodies,
                              start_date, end_date)

        graph.add_today()
        return graph.http_png()

    def symbol_url(self, identifier=None, start_date=None, end_date=None):
        return super(WorkspaceItemAdapterKrw, self).symbol_url(
            identifier=identifier,
            start_date=start_date,
            end_date=end_date,
            icon_style=ICON_STYLE[self.layer_name])

    def html(self, snippet_group=None, identifiers=None, layout_options=None):
        return super(WorkspaceItemAdapterKrw, self).html_default(
            snippet_group=snippet_group,
            identifiers=identifiers,
            layout_options=layout_options)
