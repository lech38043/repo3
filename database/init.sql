create table if not exists raw_data (
    log_id	bigint	,
    timestamp_occur	    timestamp without time zone	,
    signal_name	        character varying (200)	,
    signal_value	    character varying (200)	,
    status_value	    character varying (200)	,   
    status_description	character varying (200)	
)
