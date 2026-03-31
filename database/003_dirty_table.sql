IF OBJECT_ID('dbo.dirty_data', 'U') IS NOT NULL
DROP TABLE dbo.clean_data;
GO
CREATE TABLE dirty_data(
    [brand] NVARCHAR(50),
    [model] NVARCHAR(50),
    [price_usd] FLOAT,
    [ram_gb] FLOAT,
    [storage_gb] FLOAT,
    [camera_mp] FLOAT,
    [battery_mah] FLOAT,
    [display_size_inch] FLOAT,
    [charging_watt] FLOAT,
    [5g_support] NVARCHAR(50),
    [os] NVARCHAR(50),
    [processor] NVARCHAR(50),
    [rating] FLOAT,
    [release_month] NVARCHAR(50),
    [year] FLOAT);