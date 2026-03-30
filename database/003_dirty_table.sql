IF OBJECT_ID('dbo.dirty_data', 'U') IS NOT NULL
DROP TABLE dbo.clean_data;
GO
CREATE TABLE dirty_data(
    [brand] NVARCHAR(50),
    [model] NVARCHAR(50),
    [price_usd] BIGINT NULL,
    [ram_gb] BIGINT NULL,
    [storage_gb] BIGINT NULL,
    [camera_mp] BIGINT NULL,
    [battery_mah] BIGINT NULL,
    [display_size_inch] FLOAT,
    [charging_watt] BIGINT NULL,
    [5g_support] BIT,
    [os] NVARCHAR(50),
    [processor] NVARCHAR(50),
    [rating] FLOAT,
    [release_month] NVARCHAR(50),
    [year] BIGINT NULL);