CREATE TABLE AS_SETTINGS (
  SKEY TEXT PRIMARY KEY,
  SVALUE TEXT NOT NULL
);

INSERT INTO AS_SETTINGS VALUES ('DB_VERSION', '1');

CREATE TABLE AS_SQUARES  (
  ID INTEGER PRIMARY KEY,
  SQUARE_ID TEXT NOT NULL,
  SQUARE_DIMENSION TEXT,
  AZP TEXT,
  SURVEY_DATE TEXT,
  PEOPLE TEXT,
  PLOW_DEPTH TEXT,
  AGRO_TREATMENTS TEXT,
  WEATHER TEXT,
  TEMPERATURE TEXT,
  OBSERVATION TEXT,
  POTTERY TEXT,
  GLASS TEXT,
  BONES TEXT,
  METAL TEXT,
  FLINT TEXT,
  CLAY TEXT,
  OTHER TEXT,
  AUTHOR TEXT,
  S_REMARKS  TEXT,
  REMARKS TEXT
);

CREATE TABLE AS_SOURCES (
  ID INTEGER PRIMARY KEY,
  CHRONOLOGY TEXT,
  CULTURE TEXT,
  SQUARE INTEGER REFERENCES AS_SQUARES(ID)
);

SELECT AddGeometryColumn('AS_SQUARES', 'GEOMETRY',
  2180, 'POLYGON', 'XY', 1);

CREATE VIEW AS_RECORDS AS
SELECT S.ID AS FEATURE_ID,
       S.SQUARE_ID AS 'SQUARE ID',
       S.SQUARE_DIMENSION AS 'SQUARE DIMENSION',
       S.AZP AS 'AZP NUMBER',
       S.SURVEY_DATE AS 'SURVEY DATE',
       S.PEOPLE AS 'PEOPLE',
       S.PLOW_DEPTH AS 'PLOW DEPTH',
       S.AGRO_TREATMENTS AS 'AGRICULTURAL TREATMENTS',
       S.WEATHER AS 'WEATHER',
       S.TEMPERATURE AS 'TEMPERATURE',
       S.OBSERVATION AS 'OBSERVATION',
       S.REMARKS AS 'OBSERVATION REMARKS',
       S.POTTERY,
       S.GLASS,
       S.BONES,
       S.METAL,
       S.FLINT,
       S.CLAY,
       S.OTHER,
       X.CHRONOLOGY,
       X.CULTURE,
       S.AUTHOR,
       S.S_REMARKS AS 'SOURCES REMARKS',
       S.GEOMETRY,
       S.SQUARE_ID,
       S.SQUARE_DIMENSION,
       S.AZP,
       S.SURVEY_DATE,
       S.PEOPLE,
       S.PLOW_DEPTH,
       S.AGRO_TREATMENTS,
       S.WEATHER,
       S.TEMPERATURE,
       S.OBSERVATION,
       S.REMARKS,
       S.S_REMARKS
FROM AS_SQUARES S LEFT JOIN AS_SOURCES X ON S.ID = X.SQUARE;

INSERT INTO VIEWS_GEOMETRY_COLUMNS VALUES ('as_records', 'geometry', 'feature_id', 'as_squares', 'geometry', 1);
