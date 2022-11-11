use PredicitveIncidentManagement;
CREATE TABLE [tbl_change_request] (
	Id int NOT NULL IDENTITY(1,1),
	Date datetime NOT NULL,
	Description varchar(MAX) NOT NULL,
	Impact varchar(255) NOT NULL,
  CONSTRAINT [PK_TBL_CHANGE_REQUEST] PRIMARY KEY CLUSTERED
  (
  [Id] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [tbl_environment_change] (
	Id int NOT NULL IDENTITY(1,1),
	Date datetime NOT NULL,
	Description varchar(MAX) NOT NULL,
	Impact varchar(255) NOT NULL,
  CONSTRAINT [PK_TBL_ENVIRONMENT_CHANGE] PRIMARY KEY CLUSTERED
  (
  [Id] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [tbl_sla_lookup] (
	Id int NOT NULL UNIQUE,
	Impact varchar(255) NOT NULL,
	SLA_Time int NOT NULL,
  CONSTRAINT [PK_TBL_SLA_LOOKUP] PRIMARY KEY CLUSTERED
  (
  [Impact] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [tbl_resolution_time_lookup] (
	Id int NOT NULL IDENTITY(1,1),
	Impact varchar(255) NOT NULL,
	Incident_Type varchar(255) NOT NULL,
	Components_Subgroups varchar(500) NOT NULL,
	Resolution_Time float NOT NULL
)
GO
CREATE TABLE [tbl_incidents] (
	Id int NOT NULL IDENTITY(1,1),
	Date datetime NOT NULL,
	Incident_Number varchar(255) NOT NULL,
	Description varchar(MAX) NOT NULL,
	Impact varchar(255) NOT NULL,
  CONSTRAINT [PK_TBL_INCIDENTS] PRIMARY KEY CLUSTERED
  (
  [Id] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [tbl_incidents_predictions] (
	Id int NOT NULL IDENTITY(1,1),
	Incident_Id Int NOT NULL,
	Incident_Type varchar(255) NOT NULL,
	Subgroups varchar(500) NOT NULL, 
	Is_Change_Request bit NOT NULL,
	Is_Environmental_Change bit NOT NULL,
	Is_Service_Request bit NOT NULL,
	Average_Resolution_Time float NOT NULL,
  CONSTRAINT [PK_TBL_INCIDENTS_PREDICTIONS] PRIMARY KEY CLUSTERED
  (
  [Id] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [tbl_environment_change_predictions] (
	Id int NOT NULL IDENTITY(1,1),
	Env_Change_Id int NOT NULL,
	Incident_Type varchar(255) NOT NULL,
	Env_Subgroups varchar(500) NOT NULL,
  CONSTRAINT [PK_TBL_ENVIRONMENT_CHANGE_PREDICTIONS] PRIMARY KEY CLUSTERED
  (
  [Id] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [tbl_change_request_predictions] (
	Id int NOT NULL IDENTITY(1,1),
	CR_Incident_Id int NOT NULL,
	Incident_Type varchar(255) NOT NULL,
	CR_Subgroups varchar(500) NOT NULL,
	Previous_Component_Servers_Affected varchar(MAX) NOT NULL,
	Past_Similar_Incident_Count int NOT NULL,
	Past_Similar_Incident_Description varchar(MAX) NOT NULL,
  CONSTRAINT [PK_TBL_CHANGE_REQUEST_PREDICTIONS] PRIMARY KEY CLUSTERED
  (
  [Id] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO




ALTER TABLE [tbl_incidents] WITH CHECK ADD CONSTRAINT [tbl_incidents_fk0] FOREIGN KEY ([Impact]) REFERENCES [tbl_sla_lookup]([Impact])
ON UPDATE CASCADE
GO
ALTER TABLE [tbl_incidents] CHECK CONSTRAINT [tbl_incidents_fk0]
GO

ALTER TABLE [tbl_incidents_predictions] WITH CHECK ADD CONSTRAINT [tbl_incidents_predictions_fk0] FOREIGN KEY ([Incident_Id]) REFERENCES [tbl_incidents]([Id])
ON UPDATE CASCADE
GO
ALTER TABLE [tbl_incidents_predictions] CHECK CONSTRAINT [tbl_incidents_predictions_fk0]
GO

ALTER TABLE [tbl_environment_change_predictions] WITH CHECK ADD CONSTRAINT [tbl_environment_change_predictions_fk0] FOREIGN KEY ([Env_Change_Id]) REFERENCES [tbl_environment_change]([Id])
ON UPDATE CASCADE
GO
ALTER TABLE [tbl_environment_change_predictions] CHECK CONSTRAINT [tbl_environment_change_predictions_fk0]
GO

ALTER TABLE [tbl_change_request_predictions] WITH CHECK ADD CONSTRAINT [tbl_change_request_predictions_fk0] FOREIGN KEY ([CR_Incident_Id]) REFERENCES [tbl_change_request]([Id])
ON UPDATE CASCADE
GO
ALTER TABLE [tbl_change_request_predictions] CHECK CONSTRAINT [tbl_change_request_predictions_fk0]
GO



