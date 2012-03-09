Changelog of lizard-measure
===================================================


1.10.6 (unreleased)
-------------------

- Nothing changed yet.


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
