-- Obj storage
begin
    dbms_cloud.create_credential(
        credential_name => 'obj_store',
        username => 'livinglearninglab@gmail.com',
        password => 'AFRqpqo5{i11A[6hcl]w'
    );
end;
/
begin
    dbms_cloud.drop_credential(
        credential_name => 'obj_store');
end;
/

begin
    dbms_cloud.CREATE_CREDENTIAL(
        credential_name => 'oci_api_key',
        user_ocid => 'ocid1.user.oc1..aaaaaaaazglnlz2b2vwvtimgzicnm5ikalmvvj7zmgctyf5sdsc3675fvfla',
        tenancy_ocid => 'ocid1.tenancy.oc1..aaaaaaaawwvzqray3m54yblvqodvzwc6i5kq7jn6ygscbakqkn2xtnpznska',
        private_key => '-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC+h1+v6MyfjFCr
1YHSIO+PUdknVz0bPkf6VEwZeSeL/oFdEaXp/N0cS1ZW+cbdBGddksg7CBeRPtr6
aTybsiya4Fdubz9qmpDRQ29o6rqwLAkFlcfd5SqjIXFYB9ZBZYVSw56pivTIU3OV
EUrHczhxaGjc0puv3WkTH+UmEXvkBqm6tN3u9DUwqPy1biUHtz6b+obI1rjO9WEZ
UmAZMLSplkddgnuAgqc6a8lPxEwBL+MbRelzdrjcQ5yRlPl3KZRSrOJojzmd+Qhe
WP690oCSJf+rRDnkDP07/cyAWB1UBLA8CbNbBw8EPCcple/GCmOLVHipqy31x7qG
PLau8WVlAgMBAAECggEADSVWWahPNLOf6KNEIE/2ciXnEkWnfobhvNNufBQgbD0v
XCZjaLgc4h65Qn9cab6BNUhzOU4kdiM8mlTYLN6dIO3ZX9IcMYpK81gFoAW7biaz
qVIoJqwbsNgWCR63+UN8cJ/1BWSu4Vg6BtnZFiw3LkKnzZNYe54OvxY5yifLAQoY
HcmmM2USYvkGLdno7vwyYEwUMUhzqLAUz4RftgIhCIV6EB/FGS0DCHgareIfmWXO
yPCJGBps7aijbkitWGuxQsjnZWtQ7qzp4ToREGSsVdCCdEmm2PNN3ps33mmab/mA
7e0fkKPOeDi7ghAiqz8W8g2QcWTLla94Vq1wOgtocQKBgQDrCx9dN34oPSQ4NWYN
+TzX6VvCf94U0fOFDCeG2Aczedan3rLqvaRUvEBg0y+PZ2my7sdAyfNYb6mtuzTd
XxuQ7HJzDJJdiowCiOFoMrEAl5acbgGlkn6LZrl5tfneWhE/PySGNvuXIWyEmWNi
ThTNfKKB2mOOYhJXdWs+Yb6O/QKBgQDPhDPVoq1/acgEQ6NZC93S1MoWLQYjDQ2g
QHfg1CHZlMHTgjeU2/+44+Du5h79Vnvo0QQw4w93evVqnCHWE1WyCVy5OPqMAUfC
EXGIYfy5udcJXcT98gooKghB07+ybVzCNt/m+xxOCXxrAgzJiJRvTAH/eVqvR3I0
E7VxHzhgiQKBgHIyADYI/RlNw2gvwXquijoYncVc3Khe7SLKKfYgxTbkTj9XOrRE
GTA2Gk0wrd3Nj5Qo4NQAimOANP88gk2/pKP/zQdKp14dLzMYD/PRFSBFhh5QcCpi
h2rxKNIScOjv94s0AWnYEtp1mcS+xYOAjijcEhRm55HI4kJtwQIY+T19AoGBALH2
EynT/+wzwFd/1fcIiSxEViZcaFXo3NWgU+4YngrlWq/TjWz4mj5qFr1p1gu2fj7z
+R8fqmTxqsPJr+7R1/z9sGob5ino8ywIH5AxUDXKnRIoO0b4qiM1oK0rNcuDpDfe
LXf9w5Fc6zktod+3ZGxqB5Ca9t04bUUh3clsV8HZAoGABGvuAfsZ68ifbffv+6J9
zmc5wm2ak3Fg/uC+y/7f/yNgrX+MvbQL6kyM8vtegUlE74FjKo5UyQdVGSogdjIF
QAWdfbJz6ZRr4GhP6m2jKlu/2aulthwHBmVHUqfHmlf0Jfvge1/MfGOAngQuf/q+
bZmFlqJKudsqimFOOaTN5NE=
-----END PRIVATE KEY-----',
        fingerprint => 'fe:c7:e8:a9:0f:c9:69:06:32:ce:9b:b4:7b:db:64:b5'
    );
end;
/

SELECT *
FROM DBMS_CLOUD.LIST_OBJECTS(
  credential_name => 'oci_api_key',
  location_uri    => 'https://objectstorage.us-chicago-1.oraclecloud.com/n/axgkh7dy5i3g/b/gold/o/'
);

-- CREATE TABLES
CREATE TABLE SOURCE_APP (
    ID NUMBER PRIMARY KEY,
    NAME VARCHAR2(100) UNIQUE NOT NULL
);

insert into SOURCE_APP (ID, NAME) values (1, 'eBird');
insert into SOURCE_APP (ID, NAME) values (2, 'iNaturalist');
commit;

drop table if exists TEMP_EBIRD;

CREATE TABLE TEMP_EBIRD 
   (	
    ID VARCHAR2(64), 
	CHECKLIST_ID VARCHAR2(100), 
	OBSERVED_ON DATE,
	SPECIES_CODE VARCHAR2(200), 
	SCIENTIFIC_NAME VARCHAR2(200), 
	COMMON_NAME VARCHAR2(200), 
	HOW_MANY NUMBER, 
	LOCATION_ID VARCHAR2(200), 
	LOCATION_NAME VARCHAR2(200), 
	STATE VARCHAR2(200), 
	COUNTRY VARCHAR2(64), 
	LATITUDE NUMBER, 
	LONGITUDE NUMBER, 
	OBS_VALIDITY BOOLEAN, 
	LOADED_TIMESTAMP DATE, 
	SOURCE NUMBER
   ) ;

drop table if exists TEMP_INATURALIST;
CREATE TABLE TEMP_INATURALIST 
   (	
    ID NUMBER, 
	OBSERVED_ON TIMESTAMP (6) WITH TIME ZONE, 
	TAXON_ID NUMBER, 
	SCIENTIFIC_NAME VARCHAR2(200), 
	COMMON_NAME VARCHAR2(200), 
	RANK VARCHAR2(200), 
	NATIVE BOOLEAN, 
	THREATENED BOOLEAN, 
	PLACE_GUESS VARCHAR2(200), 
	LOCATION_NAME VARCHAR2(200),
	LATITUDE NUMBER, 
	LONGITUDE NUMBER, 
	OBS_VALIDITY VARCHAR2(200), 
	OBSERVATION_PHOTO VARCHAR2(400), 
	LOADED_TIMESTAMP DATE, 
	SOURCE NUMBER
   ) ;

drop table if exists observations;
CREATE TABLE observations
   (	
    SOURCE_OBSERVATION_ID VARCHAR2(100), 
	OBSERVED_ON TIMESTAMP (6) WITH TIME ZONE, 
  taxon_code VARCHAR2(100),
	SCIENTIFIC_NAME VARCHAR2(200), 
	COMMON_NAME VARCHAR2(200), 
    HOW_MANY NUMBER,
	RANK VARCHAR2(200), 
	LOCATION_NAME VARCHAR2(200),
	LATITUDE NUMBER, 
	LONGITUDE NUMBER, 
	VALIDITY VARCHAR2(200), 
	PHOTO VARCHAR2(400), 
	LOADED_TIMESTAMP DATE, 
	SOURCE NUMBER
   ) ;


 -- Load sources
 --- iNaturalist
 DECLARE
  l_TABLE_NAME        DBMS_QUOTED_ID := '"TEMP_INATURALIST"';
  l_CREDENTIAL_NAME   DBMS_QUOTED_ID := '"OCI_API_KEY"';
  l_FILE_URI_LIST     CLOB :=
    q'[https://objectstorage.us-chicago-1.oraclecloud.com/n/axgkh7dy5i3g/b/landing/o/observations/inaturalist/*.csv]';
  l_FIELD_LIST        CLOB :=
    q'[
     "ID"                 CHAR
    ,"OBSERVED_ON"        CHAR date_format TIMESTAMP WITH TIME ZONE MASK "YYYY-MM-DD\"T\"HH24:MI:SS.FF9TZR"
    ,"TAXON_ID"           CHAR
    ,"SCIENTIFIC_NAME"    CHAR(32767)
    ,"COMMON_NAME"        CHAR(32767)
    ,"RANK"               CHAR(32767)
    ,"NATIVE"             CHAR
    ,"THREATENED"         CHAR
    ,"PLACE_GUESS"        CHAR(32767)
    ,"LOCATION_NAME"      CHAR(32767)
    ,"LATITUDE"           CHAR
    ,"LONGITUDE"          CHAR
    ,"OBS_VALIDITY"       CHAR(32767)
    ,"OBSERVATION_PHOTO"  CHAR(32767)
    ,"LOADED_TIMESTAMP"   CHAR date_format DATE MASK "YYYY-MM-DD HH24:MI:SS"
    ,"SOURCE"             CHAR]';
  l_FORMAT            CLOB :=
    '{
       "delimiter" : ",",
       "ignoremissingcolumns" : true,
       "ignoreblanklines" : true,
       "blankasnull" : true,
       "trimspaces" : "lrtrim",
       "quote" : "\"",
       "characterset" : "AL32UTF8",
       "skipheaders" : 1,
       "logprefix" : "TEMP_INATURALIST",
       "logretention" : 7,
       "rejectlimit" : 10000000,
       "recorddelimiter" : "X''0D0A''"
     }';
  l_SCHEMA_NAME       DBMS_QUOTED_ID := '"ADMIN"';
  l_OPERATION_ID      NUMBER ; /* OUT */
BEGIN
  DBMS_CLOUD.COPY_DATA
  ( TABLE_NAME        => l_TABLE_NAME
   ,CREDENTIAL_NAME   => l_CREDENTIAL_NAME
   ,FILE_URI_LIST     => l_FILE_URI_LIST
   ,FIELD_LIST        => l_FIELD_LIST
   ,FORMAT            => l_FORMAT
   ,SCHEMA_NAME       => l_SCHEMA_NAME
   ,OPERATION_ID      => l_OPERATION_ID
  );
END;
/  

-- eBird
DECLARE
  l_TABLE_NAME        DBMS_QUOTED_ID := '"TEMP_EBIRD"';
  l_CREDENTIAL_NAME   DBMS_QUOTED_ID := '"OCI_API_KEY"';
  l_FILE_URI_LIST     CLOB :=
    q'[https://objectstorage.us-chicago-1.oraclecloud.com/n/axgkh7dy5i3g/b/landing/o/observations/ebird/*.csv]';
  l_FIELD_LIST        CLOB :=
    q'[
     "ID"                 CHAR(32767)
    ,"CHECKLIST_ID"       CHAR(32767)
    ,"OBSERVED_ON"        CHAR date_format DATE MASK "YYYY-MM-DD HH24:MI:SS"
    ,"SPECIES_CODE"       CHAR(32767)
    ,"SCIENTIFIC_NAME"    CHAR(32767)
    ,"COMMON_NAME"        CHAR(32767)
    ,"HOW_MANY"           CHAR
    ,"LOCATION_ID"        CHAR(32767)
    ,"LOCATION_NAME"      CHAR(32767)
    ,"STATE"              CHAR(32767)
    ,"COUNTRY"            CHAR(32767)
    ,"LATITUDE"           CHAR
    ,"LONGITUDE"          CHAR
    ,"OBS_VALIDITY"       CHAR
    ,"LOADED_TIMESTAMP"   CHAR date_format DATE MASK "YYYY-MM-DD HH24:MI:SS"
    ,"SOURCE"             CHAR]';
  l_FORMAT            CLOB :=
    '{
       "delimiter" : ",",
       "ignoremissingcolumns" : true,
       "ignoreblanklines" : true,
       "blankasnull" : true,
       "trimspaces" : "lrtrim",
       "quote" : "\"",
       "characterset" : "AL32UTF8",
       "skipheaders" : 1,
       "logprefix" : "TEMP_EBIRD",
       "logretention" : 7,
       "rejectlimit" : 10000000,
       "recorddelimiter" : "X''0D0A''"
     }';
  l_SCHEMA_NAME       DBMS_QUOTED_ID := '"ADMIN"';
  l_OPERATION_ID      NUMBER ; /* OUT */
BEGIN
  DBMS_CLOUD.COPY_DATA
  ( TABLE_NAME        => l_TABLE_NAME
   ,CREDENTIAL_NAME   => l_CREDENTIAL_NAME
   ,FILE_URI_LIST     => l_FILE_URI_LIST
   ,FIELD_LIST        => l_FIELD_LIST
   ,FORMAT            => l_FORMAT
   ,SCHEMA_NAME       => l_SCHEMA_NAME
   ,OPERATION_ID      => l_OPERATION_ID
  );
END;
/


-- Rebuild observations table
TRUNCATE TABLE observations;
INSERT INTO observations (
  SOURCE_OBSERVATION_ID,
    OBSERVED_ON,
    TAXON_CODE,
    SCIENTIFIC_NAME,
    COMMON_NAME,
    HOW_MANY,
    RANK,
    LOCATION_NAME,
    LATITUDE,
    LONGITUDE,
    VALIDITY,
    PHOTO,
    LOADED_TIMESTAMP,
    SOURCE
)
SELECT
    ID AS SOURCE_OBSERVATION_ID,
    OBSERVED_ON,
    species_code AS taxon_code,
    lower(SCIENTIFIC_NAME) AS SCIENTIFIC_NAME,
    lower(nvl(COMMON_NAME,SCIENTIFIC_NAME)) AS COMMON_NAME,
    nvl(HOW_MANY, 1),
    'unknown' AS RANK,
    LOCATION_NAME,
    LATITUDE,
    LONGITUDE,
    decode(OBS_VALIDITY, true, 'valid', false, 'invalid', 'unknown') AS VALIDITY,
    null AS PHOTO,
    LOADED_TIMESTAMP,
    SOURCE
FROM TEMP_EBIRD
;
commit;


INSERT INTO observations (SOURCE_OBSERVATION_ID, OBSERVED_ON, taxon_code, SCIENTIFIC_NAME, COMMON_NAME, HOW_MANY, RANK, LOCATION_NAME, LATITUDE, LONGITUDE, VALIDITY, PHOTO, LOADED_TIMESTAMP, SOURCE)
SELECT
    ID AS SOURCE_OBSERVATION_ID,
    OBSERVED_ON,
    taxon_id as taxon_code,
    lower(SCIENTIFIC_NAME) AS SCIENTIFIC_NAME,
    lower(nvl(COMMON_NAME,SCIENTIFIC_NAME)) AS COMMON_NAME,
    1 AS HOW_MANY,
    nvl(RANK, 'unknown') AS RANK,
    LOCATION_NAME,
    LATITUDE,
    LONGITUDE,
    nvl(OBS_VALIDITY, 'unknown') AS VALIDITY,
    OBSERVATION_PHOTO AS PHOTO,
    LOADED_TIMESTAMP,
    SOURCE
FROM TEMP_INATURALIST;

commit;


-- Export data to Object Storage as a CSV file

BEGIN
  DBMS_CLOUD.EXPORT_DATA(
    credential_name => 'oci_api_key',
    file_uri_list => 'https://objectstorage.us-chicago-1.oraclecloud.com/n/axgkh7dy5i3g/b/gold/o/observations/observations',
    format => JSON_OBJECT('type' VALUE 'csv', 'trimspaces' VALUE 'lrtrim', 'header' value true),
    query => 'SELECT * FROM OBSERVATIONS'
  );
END;
/


BEGIN
  DBMS_CLOUD.EXPORT_DATA(
    credential_name => 'oci_api_key',
    file_uri_list => 'https://objectstorage.us-chicago-1.oraclecloud.com/n/axgkh7dy5i3g/b/gold/o/observed_species/observed_species',
    format => JSON_OBJECT('type' VALUE 'csv', 'trimspaces' VALUE 'lrtrim', 'header' value true),
    query => 'select distinct source, species_code as taxon_code, SCIENTIFIC_NAME, common_name from TEMP_ebird
UNION ALL 
select distinct source, to_char(taxon_id) as taxon_code, SCIENTIFIC_NAME, COMMON_NAME from TEMP_INATURALIST'
  );
END;
/
