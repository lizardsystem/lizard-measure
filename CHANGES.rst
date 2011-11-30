Changelog of lizard-measure
===================================================


1.4 (unreleased)
----------------

- Renamed from lizard-krw to lizard-measure.

- Removed krw scores models and views.

- Added api for measures.

- Started new migrations. If you were using the lizard-krw, then you
  can rename the tables from prefix lizard_krw to lizard_measure and
  take it from there.


1.3 (2011-09-14)
----------------

- Fixed the problem that the graphs seemed tilted (ticket 2763). The problem
  was caused by time series data from the FEWS unblobbed database that is not
  ordered in time (where it was ordered in the past).


1.2 (2011-04-27)
----------------

- Changed lay-out of indicators of waterbodies.

- Fixed error by graph, changed date to datetime in views krw_measure_graph().


1.1 (2011-04-27)
----------------

- Updated views with date popup.

- Updated views for using lizard-map 1.60.

- Deleted action-icon ".ss_calendar_view_day" and date_popup from:
  /templates/lizard_krw/water_body_summary.html
  /templates/lizard_krw/measure_collection.html
  /templates/lizard_krw/waterbody_measures.html
  /templates/lizard_krw/krw_scores.html
  /templates/lizard_krw/measure.html

- Added Action-icon ".ss_calendar_view_day" and date_popup to:
  /templates/lizard_map/lizardgis.html
  /templates/lizard_krw/krw_scores.html


1.0.3 (2011-03-10)
------------------

- Changed shape_id to shape_slug in tiny_map (removes hardcoding your
  shape_id in urls.py).


1.0.2 (2011-02-15)
------------------

- Moved krw.png icon to app_icons subdir.

- Fixed bug with krw scores overview.


1.0 (2011-02-08)
----------------

- Improved calculations and added tests for calculation of
  status_moments and measure_status_moments.

- Updated measure screen and waterbody_measures screen.

- Added option to add MeasureCollections as well as Measures to the
  measure overview screen.

- Added fields investment_expenditure and exploitation_expenditure to
  MeasureStatusMoment.

- Removed estimated_costs_total and estimated_costs_internal from
  MeasureCollection.

- Added model ExecutivePart.

- Added model OrganizationPart.

- Refactored krw measure graph and adapter.image function.

- Added measure_collection view.

- Changed measure user from required to optional.


0.10 (2011-02-02)
-----------------

- Added model MeasureCollection, Department and corresponding
  migration.

- Added measure_collection to Measure model and migration.


0.9 (2011-02-01)
----------------

- Updated all views/templates with new breadcrumbs method.

- Updated migration 0004: on sqlite it generated an error.

- Updated summary screen with extra parameters.

- Added fields to waterbody.

- Added models Area, Province, Municipality.

- Reversed vertical order of krw measures in krw measure graph.

- Added explicit AlphaScore order ("-min_value").

- Refactored portal-tabs. Portal-tabs are now inherited from the
  (overwritten) lizard_ui/lizardbase.html.

- Refactored color fields and AlphaScore.

- Added krw scores page.

- Added legends to krw graphs in adapter/analysis.

- Added lizard_krw fixture.

- Added template parameter to krw_browser.

- Slightly changed layout of krw_browser.

- Changed required field water_type in water_body to optional with
  migration (no backwards migration).


0.8 (2010-12-22)
----------------

- Added migration.

- Added generate_measure_codes management command.


0.7 (2010-12-21)
----------------

- Updated krw score layout.

- Changed measure costs (3x) from float to integer.

- Order Organizations by name.


0.6 (2010-12-20)
----------------

- Renamed krw score classes.

- Fixed saving alpha scores. TODO: refactor goal score/alpha score/color.


0.5 (2010-12-16)
----------------

- Restarted migration steps from 0001.


0.4 (2010-12-16)
----------------

- Manually changed migrations. Not sure yet if it works correctly.


0.3 (2010-12-16)
----------------

- New measure model and accompanying models + migrations.

- Adjusted measure screen.


0.2 (2010-12-16)
----------------

- Krw adapter can now show alternative maps.

- Area_search now matches ident instead of name.

- Fixed reverse urls.

- Added WaterBody.ident.

- Added initial South migration.


0.1 (2010-12-07)
----------------

- Copy the following items from krw-waternet:

   - models
   - views
   - urls
   - templates
   - layers
   - admin
   - js/css

- Initial library skeleton created by nensskel.  [Jack]
