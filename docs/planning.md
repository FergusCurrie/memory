# Project planning

## Current state

- Simple UI + polars problem + sm2 scheduling
- Semi implementations for pyspark and sql.
  - Requires review for implementation on linux
-

## Todo

- cleaning up current questions
- says polars when its sql
- use default code
- no errors logged from sql
- default to display table
- shift enter would be really nice
- tracking number attempts?

Key:

- [ ] pull all metrics think required for good algo into save
- [ ] should multiple tries be allowed?
- [ ] default not being added to code editor
- [ ] tsql errors not handled very well.
- [ ] editing card should auto bury
- [ ] sending logs back from frontend
- [ ] code to add datasets in
- [ ] Move code completition into an interface

## Doing

- [ ] Queryable logs
- [ ]
- [ ]

## Backlog

- [ ] plotly javascript integration seems pretty good
- [ ] display table automatically
- [ ] display problem type
- [ ] simple way to regenerate database with example dbs
- [ ] filters and search on browse
- [ ] actual testing of routes. can be done with fixtures and stuff
- [ ] clean up routes
- [ ] multiple datasets
- [ ] add code should show dataset
- [ ] edit from study
- [ ] edit default code
- [ ] Interfaces frontend
- [ ] Pydantic stuff fastapi
- [ ] research logging best practices
- [ ] Tags
- [ ] Flags
- [ ] Edit card in place
- [ ] Bury
- [ ] Delte
- [ ] Profile of future reviews
- [ ] Add stats
- [ ] Record times on solutions
- [ ] MySQL for linx
- [ ] Switch tos qlalchemy
- [ ] Prevent duplicate
- [ ] Refactor scheduling into an interface
- [ ] Refactor code checks into an interface
- [ ] Refactor problems into an interface
- [ ] Improve clarity of app data model. Where data goes where
- [ ] Switch to postgres for backend
- [ ] Improve fastapi layout / implementation
- [ ] UI improvements
- [ ] Code browse improvements
- [ ] How to host on linux? Docker swarm / kubernetes for sql, pyspark, app etc.
- [ ] Review on complete, less work?
- [ ] Logging from prod? Prometheus?
- [ ] UI drop new datasets in, write to db as tables. No json please

# done

- [x] move due schedule into a database, calculate on card complete
- [x] Improved logging. Requires research of what should be logged
- [x] switch to sqlalchemy, connected to local postgres
- [x] Move scheduling into an interface
- [x] code to migrate old db in (or do jsut recreate? )
- [x] env variables

# Usability things

- editing card inplace.
- flags?
- hotkeys
- default code
- first db already visualised
- smaller databases
