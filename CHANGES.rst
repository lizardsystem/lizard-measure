Changelog of lizard-measure
===================================================


1.80.2 (unreleased)
-------------------

- Fix error on update fixure.


1.80.1 (2012-11-29)
-------------------

- Set DataSet object to measure on create pp397.


1.79.10 (2012-11-19)
--------------------

- Fixed error on open a 'maatregel' pp400, added filter 'addslashes' to measure.title. 


1.79.9 (2012-10-22)
-------------------

- Replaced limit on 'KRW Waterlichamen' filter in 'Measure' form.


1.79.8 (2012-10-11)
-------------------

- Fixed syntax errors.


1.79.7 (2012-10-08)
-------------------

- Enabled field 'Naam' in 'Maatregel' form.


1.79.6 (2012-09-26)
-------------------

- Changed field 'slecht' to 'ontoereikend' of 'ERK overzicht' overview pp381.


1.79.5 (2012-09-26)
-------------------

- Fixed filter to select submeasures per area pp376.


1.79.4 (2012-09-25)
-------------------

- Applied linebreaks filter to description field pp375.


1.79.3 (2012-09-25)
-------------------

- Changed url parameter unit-as-y-label to unit_as_y_label.

- Configured setup.py, testsettings.py to run test.


1.79.2 (2012-09-20)
-------------------

- Changed the field 'description' of Measure model to TextField, pp375.

- Added functionality to reset filters in 'Beheer/Maatregelen' form, pp370.

- Removed limit for filters 'aan/ afvoer gebieden' and 'KRW waterlichamen' in 
  'Beheer/Maatregelen' form, pp370.

- Changed 'remote call' to 'local call' for the filters 'aan/ afvoer gebieden'
  and 'KRW waterlichamen' in 'Beheer/Maatregelen' form, pp369.


1.79.1 (2012-09-18)
-------------------

- Hopefully removed dependency on Sentry.


1.79 (2012-09-18)
-----------------

- Updated import_krw_portal to update existing Areas instead of
  creating new ones.


1.78.1 (2012-07-02)
-------------------

- Added migration for HorizontalBarGraphItem because inherited class
  has changed.


1.78 (2012-06-14)
-----------------

- added userrights to views (pp 367)


1.77.2 (2012-06-12)
-------------------

- Show measure unit next to value input field. Will not update immediately
  based on measure type.


1.77.1 (2012-06-06)
-------------------

- Fix display of measure value in popup html.


1.77 (2012-06-06)
-----------------

- Remove debugger from maatregelen_form.
- ie issues (partly solve pp346)

1.76.1 (2012-06-05)
-------------------

- Move unit field from measure to measuretype and add method on measure
  to access it.

- Remove unit from form and api.


1.76 (2012-06-04)
-----------------


- Add replacement of measurecategories because imported names didn't
  map to use case names.



1.75 (2012-06-01)
-----------------

- Fix filter measure table (pp 312)


1.74 (2012-05-31)
-----------------

- Only show valid MeasureCategories in form.


1.73 (2012-05-31)
-----------------

- filter for measure table (pp 312)


1.72 (2012-05-30)
-----------------

- Organisation names must be a minimal length when edited (pp 78)
- fix stuurparameter form for area's with '+' in names (pp ??)


1.71 (2012-05-30)
-----------------

- Add manangement command to fix measure categories ('doelen').


1.70 (2012-05-30)
-----------------

- Add MeasureCategoryAdmin class.


1.69 (2012-05-30)
-----------------

- Correct validation of measureperiods during import of update data.


1.68 (2012-05-30)
-----------------

- No changes logged.


1.67 (2012-05-29)
-----------------

- splitted api for steering parameter for use in reportgenerator


1.66 (2012-05-25)
-----------------

- fixed logging in runner for sync_aquo.


1.65 (2012-05-24)
-----------------

- add ident to measure unicode string (pp 334)

- columns area wider in measure table

- repeated name in steeringparameter table (pp 333)

- changed order of EKR graph legend (pp 337)

- added task to synchronize aquo domaintables


1.64 (2012-05-10)
-----------------

- Move get_funding_organisations to Measure model.
- Add attribute history_data_view to measure.
- Add view and form to view archived measure.
- Move templatetag to lizard-history.


1.63.2 (2012-04-27)
-------------------

- Added 'constrainHeader: true, heigth: 600' to all popup windows.


1.63.1 (2012-04-27)
-------------------

- Let form pass extent to geometry editor.


1.63 (2012-04-26)
-----------------

- Removed aggregation in 1.62 (forgot to mention).

- Changed titles in measure detail of measure edit / history / sub
  measure.


1.62 (2012-04-26)
-----------------

- Measure overview: order of columns changes, "bron" is wider, changed
  text.

- Added option wide_left_ticks for measure graph.

- Changed order of fields in maatregelen_form.

- Added aan- afvoergebieden and KRW gebieden to measure detail view.

- Added parent to measure detail view.

- Improved ESF in measure detail view.

- Improved layout in measure detail view.


1.61 (2012-04-25)
-----------------

- removed area name in measure screen titles (pp 232)

- fixed refresh for measure screen after edit (pp 66, pp 200, pp 234, pp 237, pp 300)


1.60 (2012-04-25)
-----------------

- Added messagebox when removing a measure in maatregelen-beheer.


1.59 (2012-04-25)
-----------------

- Renamed english field name comment to opmerking in measure
  form. Name has to me renamed in lizard_portal.combomultiselect.


1.58 (2012-04-25)
-----------------

- Added "incl. btw" to maatregelen form fields.


1.57 (2012-04-25)
-----------------

- Restrict waterbody api to real waterbodies, whose areas have the
  area_class AREA_CLASS_KRW_WATERLICHAAM.


1.56 (2012-04-25)
-----------------

- Added textual names to ESF links.


1.55 (2012-04-25)
-----------------

- Renamed field in measure form: is doel -> is gericht op.

- Renamed field in measure summary from Deelgebied to Gebied.


1.54 (2012-04-24)
-----------------

- Fix wrong id prefilled in form for submeasures.


1.53 (2012-04-24)
-----------------

- Make krw_portaal update invalidate old periods.
- Redo undone edit of get_statusmoments.
- Only allow for valid periods in measure detail edit portal.


1.52 (2012-04-24)
-----------------

- Change order of graph measures.
- Fix error in template showing focus instead of krw.


1.51 (2012-04-24)
-----------------

- bugfix: api steering parameter would crash in some cases.

- changed name of column in organisation management screen (pp 243)

- changed order columns measure table (pp 304)


1.50 (2012-04-23)
-----------------

- added ordering of steeringparameter graphs in management screen (pp 256)

- added aan/afvoergebied in steeringparameter admin screen pp 255

- added toestand/evaluation in name pp 257

- fixed samengestelde grafieken support pp 258


1.49 (2012-04-23)
-----------------

- Added legend to ekr graph.


1.48.1 (2012-04-23)
-------------------

- Bugfix ekr graph after updating fewsnorm.


1.48 (2012-04-23)
-----------------

- Added legend_location to SteerParameterGraphs.

- Renamed legend_location to legend-location in measure_graph.

- Removed 'fews_norm_source_slug' from SteerParameterGraphs. The
  option is not needed anymore, the source is determined automatically
  in lizard_graph.


1.47.1 (2012-04-23)
-------------------

- Make realisation bar smaller.


1.47 (2012-04-23)
-----------------

- Make api measureview show invalid statuses when in use.


1.46 (2012-04-23)
-----------------

- Fixed suitable_measures: judgment -> judgement.


1.45 (2012-04-19)
-----------------

- Renamed measure graph to "maatregel(en)".

- Fixed inconsistencies between focus measures of
  krw_waterbody_measures and measure graph.


1.44 (2012-04-19)
-----------------

- Improved performance of admin HorizontalBarGraphAdmin.

- Added migrations for changes in GraphItemMixin.


1.43 (2012-04-18)
-----------------

- Added latest value/comment/timestamp to doelen-beheer.

- Added dependencies on lizard-layers. We need lizard_layers.AreaValue
  for a Score view.


1.42 (2012-04-17)
-----------------

- Change order of submeasures as well.


1.41 (2012-04-17)
-----------------

- Change 'Titel' into 'Naam'


1.40 (2012-04-17)
-----------------

- Add class to widen measure summary table Pp#146
- Implement method to get latest realised status for measure
- krw measure summary changes:
    - Fix status field
    - Remove initiator
    - Rename headings
    - Indent sub-measures
    - Change order of measures to put submeasures directly under parents
    - Replace 'no' by '-' for boolean fields

- Added comments.

- Implemented new experimental Score.judgement function based on comment.


1.39 (2012-04-17)
-----------------

- Adds a missing database migration step to support a change to one of the
  Measure fields.


1.38 (2012-04-17)
-----------------

- Removed import scores from import_krw_portaal: run
  import_krw_portaal_scores separately to update the scores.


1.37 (2012-04-17)
-----------------

- Changed model to prevent saving errors.


1.36 (2012-04-16)
-----------------

- Added target_2015 and 2027 to ScoreAdmin.

- Added import_krw_portaal_scores, splitted import_scores from
  import_krw_portaal.

- Changed Score.target_* from FloatField to CharField.

- EKR graphs now use textual targets.

- suitable measures (geschikte maatregelen) returns list of measure typse instead of measures (PP#133)


1.35 (2012-04-15)
-----------------

- code behind waterbodies (pp issue 73)

- focus added to measure table (pp issue 168)

- bug fix for saving related esf's for measure (pp issue 187)

- improvements for esf pattern editor (solving issues 229 en 230)



1.34 (2012-04-11)
-----------------

- Fixed error displaying steering parameter overview


1.33 (2012-04-10)
-----------------

- When adding a measure, you can now also choose deel aan-afvoergebieden.


1.32 (2012-04-05)
-----------------

- Remove restriction of only analists allowed to view steering parameters


1.31 (2012-04-05)
-----------------

- Added API view for WaterBody

- The maatregelen_form now uses the WaterBody API view for choosing
  krw waterbody. Before the krw waterbody combobox had Areas from
  lizard-area and that would lead to a crash.


1.30 (2012-04-05)
-----------------

- Fixed bug that could crash while saving an EsfPattern.

- Renamed view EsfPattern to EsfPatternView.


1.29 (2012-04-05)
-----------------

- Modified steeringparameter form to include examples and clearer instructions


1.28 (2012-04-04)
-----------------

- Put get_filtered_model in AreaFiltered. Applied AreaFiltered to
  ScoreView, SteeringParameterPredefinedGraph and
  SteeringParameterFreeView.


1.27 (2012-04-04)
-----------------

- Added get_filtered_model to api ScoreView, so you only get objects
  that you can see.


1.26 (2012-04-02)
-----------------

- Computation of the suitable measures uses the actual ESF pattern of the area.


1.25 (2012-04-02)
-----------------

- Change authentication for steering parameter overview.


1.24 (2012-03-30)
-----------------

- Fixes an exception when the user views scores that refer to 'hidden'
  areas. (Projectplace issue 167).


1.23 (2012-03-30)
-----------------

- Translates multiple english terms in the ESF Pattern management screen
  (Projectplace issue 143).
- Uses the full number of ESF characters .. in the ESF Pattern management screen
  (Projectplace issue 143).


1.22 (2012-03-28)
-----------------

- Add ordering to measurestatusmoments function.


1.21 (2012-03-27)
-----------------

- Made more robust when requested location does not exist.


1.20 (2012-03-27)
-----------------

- Update measure graph to only show the valid labels in the legend.


1.19 (2012-03-26)
-----------------

- Updated EKR summary again to make it slightly less ugly.


1.18 (2012-03-26)
-----------------

- Updated EKR summary to make it slightly less ugly.


1.17 (2012-03-26)
-----------------

- EKR graph and summary now uses comment as the input to calculate
  color.


1.16 (2012-03-22)
-----------------

- Made HorizontalBarView more robust to ignore failing
  graph_item.time_series.

- Updated krw_waterbody_ekr_scores view with flexible location and
  HorizontalBarGraph slug. It now shows the comments of events as
  well.


1.15 (2012-03-22)
-----------------

- Make import script update a number of existing fields as well when updating.


1.14 (2012-03-22)
-----------------

- Adapt krw portal import script for doing updates.


1.13 (2012-03-20)
-----------------

- Improved EKR details screen.


1.12 (2012-03-20)
-----------------

- Moved score_from_graph_item from HorizontalBarGraphView to model
  Score.

- Added view for ekr scores.

- Removed graph from maatregelen view, the graph is now accessed
  directly from lizard-portal.


1.11.1 (2012-03-15)
-------------------

- edit optie weggehaald bij aantal kolommen organisatie beheer

- bij import_krw_portaal de projectie weggehaald (controleren of projectie zo beter gaat)


1.11 (2012-03-12)
-----------------

- Nothing changed yet.


1.10.8 (2012-03-12)
-------------------

- Add management command to add dummy geometries to measures.


1.10.7 (2012-03-12)
-------------------

- Implements the use of a default WatertypeGroup (when none has been supplied).


1.10.6 (2012-03-12)
-------------------

- add edit screen for esfPattern
- add overview page for steer parameters
- some improvements for measure editor


1.10.5 (2012-03-09)
-------------------

- Add judgement calculation to Score model.

1.10.4 (2012-02-29)
-------------------

- Renames ``create_esf_patterns`` to ``update_db_for_suitable_measures``.


1.10.3 (2012-02-28)
-------------------

- Implements management command ``create_esf_patterns`` to create each
  WatertypeGroup, connect each KRWWatertype to the appropriate WatertypeGroup
  and connect each country-wide ESF patterns.


1.10.2 (2012-02-28)
-------------------

- Require higher lizard-history version.

- Fix date representation in history view.


1.10.1 (2012-02-28)
-------------------

- distinct on measure list

- different link for KRW an aan/afvoer measures

- implementation of free steeringparameter graphs


1.10 (2012-02-27)
-----------------

- Implements further functionality for suitable measures (beta),
  issue lizardsystem/lizard-portal#18.


1.9 (2012-02-24)
----------------

- Adds initial support for suitable measures (beta),
  issue lizardsystem/lizard-portal#18.


1.8 (2012-02-17)
----------------

- Changed valid field from NullBoolean to boolean

- Add migrations

- Add total costs and land costs fields

- Add history details view


- Add extra cost fields

- Add this fields to Measure form

- Add extra fields to Measuregrid

- implement generic summary popup

- implement sortable property for column configuration for Measure grid

- Truncate datetimestring to minutes via template tag

- Add indication submeasure to waterbody_measures

- Add legend location to urls of waterbody_measures and measure templates

- Add submeasure table with links to submeasures in measure view

- Add various vields to measure detail view


1.7.1 (2012-02-16)
------------------

- Fixed measure graph x-lim.


1.7 (2012-02-16)
----------------

- The measure graph now uses nens-graph, which makes the graph
  consistent with other graphs.

- Make krw portal import script backwards compatible

- Make sync_aquo management command work on Ubuntu 10

- added distinct to measure selection for graph

- removed double entry in measure form (field focus measure)


1.6.2 (2012-02-13)
------------------

- Fix graph not loading on measuredetail view

- Add link to history page on measuredetail page

- add read only functionality to organization-management

- some migrations

- removed unique constraint on organizations

- changed EKF model to EsfLink model

- measure graph request for all parameters as parameter instead of url


1.6.1 (2012-02-09)
------------------

- Added natural keys for MeasuringRod (they are synced using
  import_krw_portaal).


1.6 (2012-02-09)
----------------

- Added default Score to EKR graph. When the score is not found in the
  database, the label will be in parentheses.

- Fixed measure graph

- Extend waterbody_measure according to use case

- Fixed doel management screen (api and gridview)

- Add EKF model

- Several smaller improvements on importscript and model

- Moved HorizontalBarGraph View and models from lizard-graph to here


1.5.8 (2012-01-31)
------------------

- added forms and sort functionality to api


1.5.7 (2012-01-30)
------------------

- Improves geometry imports in import script

- Populates data_set attributes of both areas and measures from krw-portal
  data.


1.5.6 (2012-01-26)
------------------

- Adjusts krw portal import script to use owa geometries.


1.5.5 (2012-01-13)
------------------

- Forgot to pull first. Quick re-release.


1.5.4 (2012-01-13)
------------------

- added doelen-beheer

- improved api and measure forms


1.5.3 (2012-01-24)
------------------

- Adds lizard-security

- Improves import script

- Adds portal templates for use with lizard-portal


1.5.2 (2012-01-19)
------------------

- Changes type of import_source field to IntegerField

- Adds choices to import_source field of Measures

- Adds a dummy test for buildbot


1.5.1 (2012-01-19)
------------------

- Adds synchronization code to synchronize with aquo domain tables

- Configures involved models to work with the synchronization code

- Adds bin/django sync_aquo management command to run all synchronizations


1.5 (2012-01-12)
----------------

- This release marks a big change migrating the app from the krw-waternet
  structure into the new krw-portaal-ready structure. Note that migrations
  4 and 5 throw all tables away from previous migrations and versions and
  build an entire new table set. All data present migrating to 1.5 will
  be lost.

- Models, admin and KRW-portal import script have been revamped to
  accomodate KRW-portal data and meet VSS specifications.


1.4.2 (2011-12-27)
------------------

- Renamed remaining txt-files to rst


1.4.1 (2011-12-27)
------------------

- Renamed TODO from txt to rst


1.4 (2011-12-27)
----------------

- Migrations and models.py are in a state that a specific fixture from krw-waternet
  can be loaded

- Renamed from lizard-krw to lizard-measure.

- Removed krw scores models, views and dependencies.

- Added api for measures.

- Started new migrations. If you were using the lizard-krw, then you
  can migrate to the newest migration, then rename the tables from
  prefix lizard_krw to lizard_measure and take it from there.


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
