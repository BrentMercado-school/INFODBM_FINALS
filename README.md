USE [master]
GO
/****** Object:  Database [INFODBM_FINALS]    Script Date: 12/07/2026 9:53:21 pm ******/
CREATE DATABASE [INFODBM_FINALS]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'INFODBM_FINALS', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\INFODBM_FINALS.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'INFODBM_FINALS_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\INFODBM_FINALS_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [INFODBM_FINALS] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [INFODBM_FINALS].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [INFODBM_FINALS] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET ARITHABORT OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [INFODBM_FINALS] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [INFODBM_FINALS] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET  DISABLE_BROKER 
GO
ALTER DATABASE [INFODBM_FINALS] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [INFODBM_FINALS] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [INFODBM_FINALS] SET  MULTI_USER 
GO
ALTER DATABASE [INFODBM_FINALS] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [INFODBM_FINALS] SET DB_CHAINING OFF 
GO
ALTER DATABASE [INFODBM_FINALS] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [INFODBM_FINALS] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [INFODBM_FINALS] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [INFODBM_FINALS] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [INFODBM_FINALS] SET QUERY_STORE = ON
GO
ALTER DATABASE [INFODBM_FINALS] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [INFODBM_FINALS]
GO
/****** Object:  Table [dbo].[BorrowForms]    Script Date: 12/07/2026 9:53:21 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[BorrowForms](
	[BorrowFormID] [int] IDENTITY(1,1) NOT NULL,
	[BorrowerID] [int] NOT NULL,
	[ItemID] [int] NOT NULL,
	[StartDate] [date] NOT NULL,
	[ReturnDate] [date] NOT NULL,
	[Status] [varchar](20) NOT NULL,
	[CreatedAt] [datetime] NOT NULL,
	[ApprovedAt] [datetime] NULL,
	[SecurityDepositSnapShot] [smallmoney] NOT NULL,
	[DeclineReason] [varchar](100) NULL,
 CONSTRAINT [PK_BorrowForms] PRIMARY KEY CLUSTERED 
(
	[BorrowFormID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Categories]    Script Date: 12/07/2026 9:53:21 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Categories](
	[CategoryID] [int] IDENTITY(1,1) NOT NULL,
	[Name] [varchar](50) NOT NULL,
	[CreatedAt] [datetime] NOT NULL,
	[IsActive] [bit] NOT NULL,
 CONSTRAINT [PK_Categories] PRIMARY KEY CLUSTERED 
(
	[CategoryID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [IX_Categories] UNIQUE NONCLUSTERED 
(
	[Name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Items]    Script Date: 12/07/2026 9:53:21 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Items](
	[ItemID] [int] IDENTITY(1,1) NOT NULL,
	[Name] [varchar](100) NOT NULL,
	[CategoryID] [int] NOT NULL,
	[Condition] [varchar](50) NOT NULL,
	[Description] [varchar](255) NULL,
	[Note] [varchar](255) NULL,
	[OwnerID] [int] NOT NULL,
	[ImageURL] [varchar](255) NULL,
	[SecurityDeposit] [smallmoney] NOT NULL,
	[Status] [varchar](20) NOT NULL,
	[CreatedAt] [datetime] NOT NULL,
	[UpdatedAt] [datetime] NULL,
 CONSTRAINT [PK_Items] PRIMARY KEY CLUSTERED 
(
	[ItemID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ReturnForms]    Script Date: 12/07/2026 9:53:21 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ReturnForms](
	[ReturnFormID] [int] IDENTITY(1,1) NOT NULL,
	[BorrowFormID] [int] NOT NULL,
	[ActualReturnDate] [date] NULL,
	[DamageFee] [smallmoney] NOT NULL,
	[LatePenalty] [smallmoney] NOT NULL,
	[CreatedAt] [datetime] NOT NULL,
 CONSTRAINT [PK_ReturnForms] PRIMARY KEY CLUSTERED 
(
	[ReturnFormID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [IX_ReturnForms] UNIQUE NONCLUSTERED 
(
	[BorrowFormID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Users]    Script Date: 12/07/2026 9:53:21 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Users](
	[UserID] [int] IDENTITY(1,1) NOT NULL,
	[Username] [varchar](100) NOT NULL,
	[PasswordHash] [varchar](255) NOT NULL,
	[Address] [varchar](150) NULL,
	[ContactNumber] [varchar](20) NULL,
	[ImageURL] [varchar](255) NULL,
	[CreatedAt] [datetime] NOT NULL,
	[UpdatedAt] [datetime] NULL,
	[IsActive] [bit] NOT NULL,
 CONSTRAINT [PK_Users] PRIMARY KEY CLUSTERED 
(
	[UserID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [IX_Users] UNIQUE NONCLUSTERED 
(
	[Username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[BorrowForms] ADD  CONSTRAINT [DF_BorrowForms_CreatedAt]  DEFAULT (getdate()) FOR [CreatedAt]
GO
ALTER TABLE [dbo].[Categories] ADD  CONSTRAINT [DF_Categories_CreatedAt]  DEFAULT (getdate()) FOR [CreatedAt]
GO
ALTER TABLE [dbo].[Categories] ADD  CONSTRAINT [DF_Categories_IsActive]  DEFAULT ((1)) FOR [IsActive]
GO
ALTER TABLE [dbo].[Items] ADD  CONSTRAINT [DF_Items_SecurityDeposit]  DEFAULT ((0)) FOR [SecurityDeposit]
GO
ALTER TABLE [dbo].[Items] ADD  CONSTRAINT [DF_Items_Status]  DEFAULT ('Available') FOR [Status]
GO
ALTER TABLE [dbo].[Items] ADD  CONSTRAINT [DF_Items_CreatedAt]  DEFAULT (getdate()) FOR [CreatedAt]
GO
ALTER TABLE [dbo].[ReturnForms] ADD  CONSTRAINT [DF_ReturnForms_DamageFee]  DEFAULT ((0)) FOR [DamageFee]
GO
ALTER TABLE [dbo].[ReturnForms] ADD  CONSTRAINT [DF_ReturnForms_LatePenalty]  DEFAULT ((0)) FOR [LatePenalty]
GO
ALTER TABLE [dbo].[ReturnForms] ADD  CONSTRAINT [DF_ReturnForms_CreatedAt]  DEFAULT (getdate()) FOR [CreatedAt]
GO
ALTER TABLE [dbo].[Users] ADD  CONSTRAINT [DF_Users_CreatedAt]  DEFAULT (getdate()) FOR [CreatedAt]
GO
ALTER TABLE [dbo].[Users] ADD  CONSTRAINT [DF_Users_IsActive]  DEFAULT ((1)) FOR [IsActive]
GO
ALTER TABLE [dbo].[BorrowForms]  WITH CHECK ADD  CONSTRAINT [FK_BorrowForms_Items] FOREIGN KEY([ItemID])
REFERENCES [dbo].[Items] ([ItemID])
GO
ALTER TABLE [dbo].[BorrowForms] CHECK CONSTRAINT [FK_BorrowForms_Items]
GO
ALTER TABLE [dbo].[BorrowForms]  WITH CHECK ADD  CONSTRAINT [FK_BorrowForms_ReturnForms] FOREIGN KEY([BorrowFormID])
REFERENCES [dbo].[ReturnForms] ([BorrowFormID])
GO
ALTER TABLE [dbo].[BorrowForms] CHECK CONSTRAINT [FK_BorrowForms_ReturnForms]
GO
ALTER TABLE [dbo].[BorrowForms]  WITH CHECK ADD  CONSTRAINT [FK_BorrowForms_Users] FOREIGN KEY([BorrowerID])
REFERENCES [dbo].[Users] ([UserID])
GO
ALTER TABLE [dbo].[BorrowForms] CHECK CONSTRAINT [FK_BorrowForms_Users]
GO
ALTER TABLE [dbo].[Items]  WITH CHECK ADD  CONSTRAINT [FK_Items_Categories] FOREIGN KEY([CategoryID])
REFERENCES [dbo].[Categories] ([CategoryID])
GO
ALTER TABLE [dbo].[Items] CHECK CONSTRAINT [FK_Items_Categories]
GO
ALTER TABLE [dbo].[Items]  WITH CHECK ADD  CONSTRAINT [FK_Items_Users] FOREIGN KEY([OwnerID])
REFERENCES [dbo].[Users] ([UserID])
GO
ALTER TABLE [dbo].[Items] CHECK CONSTRAINT [FK_Items_Users]
GO
ALTER TABLE [dbo].[BorrowForms]  WITH CHECK ADD  CONSTRAINT [CK_BorrowForms_SecurityDepositSnapshot] CHECK  (([SecurityDepositSnapShot]>=(0)))
GO
ALTER TABLE [dbo].[BorrowForms] CHECK CONSTRAINT [CK_BorrowForms_SecurityDepositSnapshot]
GO
ALTER TABLE [dbo].[BorrowForms]  WITH CHECK ADD  CONSTRAINT [CK_BorrowForms_StartDate] CHECK  (([StartDate]<=[ReturnDate]))
GO
ALTER TABLE [dbo].[BorrowForms] CHECK CONSTRAINT [CK_BorrowForms_StartDate]
GO
ALTER TABLE [dbo].[BorrowForms]  WITH CHECK ADD  CONSTRAINT [CK_BorrowForms_Status] CHECK  (([Status]='Cancelled' OR [Status]='Overdue' OR [Status]='Returned' OR [Status]='Declined' OR [Status]='Accepted' OR [Status]='Pending'))
GO
ALTER TABLE [dbo].[BorrowForms] CHECK CONSTRAINT [CK_BorrowForms_Status]
GO
ALTER TABLE [dbo].[Items]  WITH CHECK ADD  CONSTRAINT [CK_Items_SecurityDeposit] CHECK  (([SecurityDeposit]>=(0)))
GO
ALTER TABLE [dbo].[Items] CHECK CONSTRAINT [CK_Items_SecurityDeposit]
GO
ALTER TABLE [dbo].[Items]  WITH CHECK ADD  CONSTRAINT [CK_Items_Status] CHECK  (([Status]='Available' OR [Status]='Borrowed' OR [Status]='Unavailable'))
GO
ALTER TABLE [dbo].[Items] CHECK CONSTRAINT [CK_Items_Status]
GO
ALTER TABLE [dbo].[ReturnForms]  WITH CHECK ADD  CONSTRAINT [CK_ReturnForms_DamageFee] CHECK  (([DamageFee]>=(0)))
GO
ALTER TABLE [dbo].[ReturnForms] CHECK CONSTRAINT [CK_ReturnForms_DamageFee]
GO
ALTER TABLE [dbo].[ReturnForms]  WITH CHECK ADD  CONSTRAINT [CK_ReturnForms_LatePenalty] CHECK  (([LatePenalty]>=(0)))
GO
ALTER TABLE [dbo].[ReturnForms] CHECK CONSTRAINT [CK_ReturnForms_LatePenalty]
GO
/****** Object:  StoredProcedure [dbo].[uspAddItem]    Script Date: 12/07/2026 9:53:21 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspAddItem]
		@name varchar(100),
		@category int,
		@condition varchar(50),
		@description varchar(255),
		@note varchar(255),
		@owner int,
		@image varchar(255),
		@securityDeposit smallmoney
	AS
	BEGIN
		SET NOCOUNT ON
	
		IF @name IS NULL OR @name = ''
		BEGIN
			SELECT 'NO NAME' as RESULT
			RETURN
		END

		IF @category IS NULL
		BEGIN
			SELECT 'NO CATEGORY' as RESULT
			RETURN
		END

		IF @condition IS NULL OR @condition = ''
		BEGIN
			SELECT 'NO CONDITION' as RESULT
			RETURN
		END

		INSERT Items ([Name], CategoryID, Condition, [Description], Note, OwnerID, ImageURL, SecurityDeposit)
		VALUES (@name, @category, @condition, @description, @note, @owner, @image, @securityDeposit)

		SELECT SCOPE_IDENTITY() AS ItemID
	END
GO
/****** Object:  StoredProcedure [dbo].[uspLoadCategories]    Script Date: 12/07/2026 9:53:21 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspLoadCategories]
AS
BEGIN
	SET NOCOUNT ON

	SELECT
		CategoryID
		,[Name] as CategoryName
	FROM Categories
	WHERE IsActive = 1
END
GO
/****** Object:  StoredProcedure [dbo].[uspLoadCommunityItems]    Script Date: 12/07/2026 9:53:21 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspLoadCommunityItems]
	@user_id int
AS
BEGIN
	SET NOCOUNT ON
	
	SELECT  
		i.ItemID
		, i.ImageURL
		, i.[Name] as ItemName
		, c.[Name] as CategoryName
		, i.Condition
		, o.Username
		, i.SecurityDeposit
		, i.[Status]
	FROM Items i JOIN  Categories c
	ON i.CategoryID = c.CategoryID JOIN Users o
	ON  i.OwnerID = o.UserID
	WHERE OwnerID <> @user_id
END
GO
/****** Object:  StoredProcedure [dbo].[uspLoginUser]    Script Date: 12/07/2026 9:53:21 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspLoginUser]
	@username varchar(100)
AS
BEGIN
	SELECT
		UserID
		, Username
		, PasswordHash
		, [Address]
		, ContactNumber
		, ImageURL
		, IsActive
	FROM Users
	WHERE Username = @username
END
GO
/****** Object:  StoredProcedure [dbo].[uspRegisterUser]    Script Date: 12/07/2026 9:53:21 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspRegisterUser]
	@username varchar(100),
	@password varchar(255)
AS
BEGIN
	SET NOCOUNT ON
	IF @username IS NULL OR LTRIM(RTRIM(@username)) = ''
	BEGIN
		SELECT 'NO USERNAME' AS Result
		RETURN
	END

	IF @password IS NULL OR @password = ''
	BEGIN
		SELECT 'NO PASSWORD' AS Result
		RETURN
	END

	IF EXISTS(SELECT 1 FROM Users WHERE Username = @username)
	BEGIN
		SELECT 'USERNAME ALREADY TAKEN' AS Result
		RETURN
	END

	INSERT Users (Username, PasswordHash)
	VALUES (@username, @password)

	SELECT 'SUCCESS' AS Result
END
GO
USE [master]
GO
ALTER DATABASE [INFODBM_FINALS] SET  READ_WRITE 
GO
