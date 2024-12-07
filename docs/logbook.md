# Tracking

- 10th November 2024

  - Cloned repo to my linux machine. Fixed bug with datasets displaying.

- 16th november

  - added logging config for hierarchical logs.
  - add docker compose to spin up a postgres instance

- 2nd december

  - updated some imports for new location of scheduling / code execution. still needs lots of work to correctly integrate the postgres stuff
  - added a way to load csv into postgres
  - added a markdown file for planning migration to postgres
  - add simple database testing
  - added simple crud functionality
  - !!! working on: creating code to add new card, need to update polling available datasets. !!!

- 4th december

  - fixed polling available datasets
  - check code on card creation now works for polars
  - !!! working on creating new problem from ui. getting error on array type for dataset names (see models.py) !!!

- 6th december

  - simple card adding available
  - NOTE: a simple approach to achieve my aims, would be to not change UI too much. Make it work similar to previously, just with clean backend. This way I could have polars/TSQL running over holidays
  - review tests, simple fetching of polars problem, following ^
  - table in polars problem being correctly sent back to ui
  - basic polars check code working. NOTE: preprocessing is overhead. Just cook up a new dataset.
  - reviews for polars prob seem to be working
  - basic functionality is up.
  - added code to input old db simple polars into db
  - browse updated to work (edits not possible)
  - suspend added
  - buried added
  - card update from ui working
  - new tsql container spun up, with initial datasets added
    - would be good to streamline this to create db when required + new datasets added to both psql, tsql.

- 7th december
  - added alembic for db migrations
  - used alembic to make type and default code columns of code
  - moved secrets to env
  - cleaned up code check code
  - added page to upload csv which gets saved to pg, tsql and datasets table
