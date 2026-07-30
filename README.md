USE [master]
GO
/****** Object:  Database [INFODBM_FINALS]    Script Date: 30/07/2026 9:45:41 pm ******/
CREATE DATABASE [INFODBM_FINALS]
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
/****** Object:  UserDefinedFunction [dbo].[fnCalculateLatePenalty]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE FUNCTION [dbo].[fnCalculateLatePenalty]
(
    @expected_return date,
    @actual_return date
)
RETURNS smallmoney
AS
BEGIN
    DECLARE @days_late int;
    DECLARE @penalty smallmoney;

    SET @days_late = DATEDIFF(DAY, @expected_return, @actual_return);

    IF @days_late < 0
        SET @days_late = 0;

    SET @penalty = @days_late * 50; 

    RETURN @penalty;
END
GO
/****** Object:  UserDefinedFunction [dbo].[fnFormatDate]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE FUNCTION [dbo].[fnFormatDate]
(
    @date date
)
RETURNS varchar(30)
AS
BEGIN
    IF @date IS NULL
        RETURN NULL

    RETURN FORMAT(@date, 'MMMM d, yyyy')
END

GO
/****** Object:  UserDefinedFunction [dbo].[fnGetOnGoingRequestStatus]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE FUNCTION [dbo].[fnGetOnGoingRequestStatus]
(
    @return_date date
)
RETURNS varchar(9)
AS
BEGIN
    DECLARE @today date = CAST(GETDATE() AS date)

    IF @return_date = @today
        RETURN 'Due Today'

    IF @return_date > @today
        RETURN 'On Track'

    RETURN 'Overdue'
END
GO
/****** Object:  Table [dbo].[BorrowForms]    Script Date: 30/07/2026 9:45:41 pm ******/
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
/****** Object:  Table [dbo].[Categories]    Script Date: 30/07/2026 9:45:41 pm ******/
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
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Items]    Script Date: 30/07/2026 9:45:41 pm ******/
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
/****** Object:  Table [dbo].[ReturnForms]    Script Date: 30/07/2026 9:45:41 pm ******/
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
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Users]    Script Date: 30/07/2026 9:45:41 pm ******/
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
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[BorrowForms] ON 

INSERT [dbo].[BorrowForms] ([BorrowFormID], [BorrowerID], [ItemID], [StartDate], [ReturnDate], [Status], [CreatedAt], [ApprovedAt], [SecurityDepositSnapShot], [DeclineReason]) VALUES (1, 2, 4, CAST(N'2026-07-01' AS Date), CAST(N'2026-07-10' AS Date), N'Accepted', CAST(N'2026-07-30T17:45:51.837' AS DateTime), CAST(N'2026-07-30T17:45:51.837' AS DateTime), 300.0000, NULL)
INSERT [dbo].[BorrowForms] ([BorrowFormID], [BorrowerID], [ItemID], [StartDate], [ReturnDate], [Status], [CreatedAt], [ApprovedAt], [SecurityDepositSnapShot], [DeclineReason]) VALUES (2, 3, 8, CAST(N'2026-07-05' AS Date), CAST(N'2026-07-15' AS Date), N'Accepted', CAST(N'2026-07-30T17:45:51.837' AS DateTime), CAST(N'2026-07-30T17:45:51.837' AS DateTime), 600.0000, NULL)
INSERT [dbo].[BorrowForms] ([BorrowFormID], [BorrowerID], [ItemID], [StartDate], [ReturnDate], [Status], [CreatedAt], [ApprovedAt], [SecurityDepositSnapShot], [DeclineReason]) VALUES (3, 4, 1, CAST(N'2026-08-01' AS Date), CAST(N'2026-08-05' AS Date), N'Pending', CAST(N'2026-07-30T17:45:51.837' AS DateTime), NULL, 200.0000, NULL)
INSERT [dbo].[BorrowForms] ([BorrowFormID], [BorrowerID], [ItemID], [StartDate], [ReturnDate], [Status], [CreatedAt], [ApprovedAt], [SecurityDepositSnapShot], [DeclineReason]) VALUES (4, 5, 3, CAST(N'2026-08-02' AS Date), CAST(N'2026-08-08' AS Date), N'Pending', CAST(N'2026-07-30T17:45:51.837' AS DateTime), NULL, 500.0000, NULL)
INSERT [dbo].[BorrowForms] ([BorrowFormID], [BorrowerID], [ItemID], [StartDate], [ReturnDate], [Status], [CreatedAt], [ApprovedAt], [SecurityDepositSnapShot], [DeclineReason]) VALUES (5, 6, 6, CAST(N'2026-08-03' AS Date), CAST(N'2026-08-06' AS Date), N'Pending', CAST(N'2026-07-30T17:45:51.837' AS DateTime), NULL, 400.0000, NULL)
INSERT [dbo].[BorrowForms] ([BorrowFormID], [BorrowerID], [ItemID], [StartDate], [ReturnDate], [Status], [CreatedAt], [ApprovedAt], [SecurityDepositSnapShot], [DeclineReason]) VALUES (6, 7, 2, CAST(N'2026-07-20' AS Date), CAST(N'2026-07-25' AS Date), N'Declined', CAST(N'2026-07-30T17:45:51.837' AS DateTime), NULL, 150.0000, N'Item not available on those dates')
INSERT [dbo].[BorrowForms] ([BorrowFormID], [BorrowerID], [ItemID], [StartDate], [ReturnDate], [Status], [CreatedAt], [ApprovedAt], [SecurityDepositSnapShot], [DeclineReason]) VALUES (7, 8, 5, CAST(N'2026-07-18' AS Date), CAST(N'2026-07-22' AS Date), N'Cancelled', CAST(N'2026-07-30T17:45:51.837' AS DateTime), NULL, 250.0000, NULL)
INSERT [dbo].[BorrowForms] ([BorrowFormID], [BorrowerID], [ItemID], [StartDate], [ReturnDate], [Status], [CreatedAt], [ApprovedAt], [SecurityDepositSnapShot], [DeclineReason]) VALUES (8, 9, 7, CAST(N'2026-06-01' AS Date), CAST(N'2026-06-10' AS Date), N'Returned', CAST(N'2026-07-30T17:45:51.837' AS DateTime), CAST(N'2026-06-01T00:00:00.000' AS DateTime), 100.0000, NULL)
INSERT [dbo].[BorrowForms] ([BorrowFormID], [BorrowerID], [ItemID], [StartDate], [ReturnDate], [Status], [CreatedAt], [ApprovedAt], [SecurityDepositSnapShot], [DeclineReason]) VALUES (9, 10, 9, CAST(N'2026-06-05' AS Date), CAST(N'2026-06-12' AS Date), N'Returned', CAST(N'2026-07-30T17:45:51.837' AS DateTime), CAST(N'2026-06-05T00:00:00.000' AS DateTime), 50.0000, NULL)
INSERT [dbo].[BorrowForms] ([BorrowFormID], [BorrowerID], [ItemID], [StartDate], [ReturnDate], [Status], [CreatedAt], [ApprovedAt], [SecurityDepositSnapShot], [DeclineReason]) VALUES (10, 1, 10, CAST(N'2026-06-15' AS Date), CAST(N'2026-06-20' AS Date), N'Returned', CAST(N'2026-07-30T17:45:51.837' AS DateTime), CAST(N'2026-06-15T00:00:00.000' AS DateTime), 180.0000, NULL)
SET IDENTITY_INSERT [dbo].[BorrowForms] OFF
GO
SET IDENTITY_INSERT [dbo].[Categories] ON 

INSERT [dbo].[Categories] ([CategoryID], [Name], [CreatedAt], [IsActive]) VALUES (1, N'Appliance', CAST(N'2026-07-30T17:45:17.773' AS DateTime), 1)
INSERT [dbo].[Categories] ([CategoryID], [Name], [CreatedAt], [IsActive]) VALUES (2, N'Technology', CAST(N'2026-07-30T17:45:17.773' AS DateTime), 1)
INSERT [dbo].[Categories] ([CategoryID], [Name], [CreatedAt], [IsActive]) VALUES (3, N'Sport', CAST(N'2026-07-30T17:45:17.773' AS DateTime), 1)
SET IDENTITY_INSERT [dbo].[Categories] OFF
GO
SET IDENTITY_INSERT [dbo].[Items] ON 

INSERT [dbo].[Items] ([ItemID], [Name], [CategoryID], [Condition], [Description], [Note], [OwnerID], [ImageURL], [SecurityDeposit], [Status], [CreatedAt], [UpdatedAt]) VALUES (1, N'Electric Drill', 1, N'Like new', N'Cordless power drill', N'Handle with care', 1, NULL, 200.0000, N'Available', CAST(N'2026-07-30T17:45:51.827' AS DateTime), NULL)
INSERT [dbo].[Items] ([ItemID], [Name], [CategoryID], [Condition], [Description], [Note], [OwnerID], [ImageURL], [SecurityDeposit], [Status], [CreatedAt], [UpdatedAt]) VALUES (2, N'Air Fryer', 1, N'Good', N'5L capacity air fryer', N'Clean after use', 1, NULL, 150.0000, N'Available', CAST(N'2026-07-30T17:45:51.827' AS DateTime), NULL)
INSERT [dbo].[Items] ([ItemID], [Name], [CategoryID], [Condition], [Description], [Note], [OwnerID], [ImageURL], [SecurityDeposit], [Status], [CreatedAt], [UpdatedAt]) VALUES (3, N'Laptop', 2, N'Slightly used', N'Core i5 laptop', N'No food near it', 2, NULL, 500.0000, N'Available', CAST(N'2026-07-30T17:45:51.827' AS DateTime), NULL)
INSERT [dbo].[Items] ([ItemID], [Name], [CategoryID], [Condition], [Description], [Note], [OwnerID], [ImageURL], [SecurityDeposit], [Status], [CreatedAt], [UpdatedAt]) VALUES (4, N'Bicycle', 3, N'Good', N'Mountain bike 26 inch', N'Return with full air', 3, NULL, 300.0000, N'Borrowed', CAST(N'2026-07-30T17:45:51.827' AS DateTime), NULL)
INSERT [dbo].[Items] ([ItemID], [Name], [CategoryID], [Condition], [Description], [Note], [OwnerID], [ImageURL], [SecurityDeposit], [Status], [CreatedAt], [UpdatedAt]) VALUES (5, N'Tent', 3, N'Like new', N'4-person camping tent', N'Dry before returning', 3, NULL, 250.0000, N'Available', CAST(N'2026-07-30T17:45:51.827' AS DateTime), NULL)
INSERT [dbo].[Items] ([ItemID], [Name], [CategoryID], [Condition], [Description], [Note], [OwnerID], [ImageURL], [SecurityDeposit], [Status], [CreatedAt], [UpdatedAt]) VALUES (6, N'Projector', 2, N'Good', N'HD projector', N'Bring your own cable', 4, NULL, 400.0000, N'Available', CAST(N'2026-07-30T17:45:51.827' AS DateTime), NULL)
INSERT [dbo].[Items] ([ItemID], [Name], [CategoryID], [Condition], [Description], [Note], [OwnerID], [ImageURL], [SecurityDeposit], [Status], [CreatedAt], [UpdatedAt]) VALUES (7, N'Blender', 1, N'Fair', N'Heavy duty blender', N'For fruits only', 5, NULL, 100.0000, N'Available', CAST(N'2026-07-30T17:45:51.827' AS DateTime), NULL)
INSERT [dbo].[Items] ([ItemID], [Name], [CategoryID], [Condition], [Description], [Note], [OwnerID], [ImageURL], [SecurityDeposit], [Status], [CreatedAt], [UpdatedAt]) VALUES (8, N'Camera', 2, N'Like new', N'DSLR camera with lens', N'Do not drop', 6, NULL, 600.0000, N'Borrowed', CAST(N'2026-07-30T17:45:51.827' AS DateTime), NULL)
INSERT [dbo].[Items] ([ItemID], [Name], [CategoryID], [Condition], [Description], [Note], [OwnerID], [ImageURL], [SecurityDeposit], [Status], [CreatedAt], [UpdatedAt]) VALUES (9, N'Basketball', 3, N'Good', N'Official size basketball', N'Indoor use preferred', 7, NULL, 50.0000, N'Available', CAST(N'2026-07-30T17:45:51.827' AS DateTime), NULL)
INSERT [dbo].[Items] ([ItemID], [Name], [CategoryID], [Condition], [Description], [Note], [OwnerID], [ImageURL], [SecurityDeposit], [Status], [CreatedAt], [UpdatedAt]) VALUES (10, N'Microwave', 1, N'Good', N'20L microwave oven', N'Handle with care', 8, NULL, 180.0000, N'Available', CAST(N'2026-07-30T17:45:51.827' AS DateTime), NULL)
SET IDENTITY_INSERT [dbo].[Items] OFF
GO
SET IDENTITY_INSERT [dbo].[ReturnForms] ON 

INSERT [dbo].[ReturnForms] ([ReturnFormID], [BorrowFormID], [ActualReturnDate], [DamageFee], [LatePenalty], [CreatedAt]) VALUES (1, 8, CAST(N'2026-06-10' AS Date), 0.0000, 0.0000, CAST(N'2026-07-30T17:45:51.887' AS DateTime))
INSERT [dbo].[ReturnForms] ([ReturnFormID], [BorrowFormID], [ActualReturnDate], [DamageFee], [LatePenalty], [CreatedAt]) VALUES (2, 9, CAST(N'2026-06-14' AS Date), 20.0000, 100.0000, CAST(N'2026-07-30T17:45:51.887' AS DateTime))
INSERT [dbo].[ReturnForms] ([ReturnFormID], [BorrowFormID], [ActualReturnDate], [DamageFee], [LatePenalty], [CreatedAt]) VALUES (3, 10, CAST(N'2026-06-20' AS Date), 0.0000, 0.0000, CAST(N'2026-07-30T17:45:51.887' AS DateTime))
SET IDENTITY_INSERT [dbo].[ReturnForms] OFF
GO
SET IDENTITY_INSERT [dbo].[Users] ON 

INSERT [dbo].[Users] ([UserID], [Username], [PasswordHash], [Address], [ContactNumber], [ImageURL], [CreatedAt], [UpdatedAt], [IsActive]) VALUES (1, N'juan', N'scrypt:32768:8:1$obXsaIdGm90VSAvr$bcd5b19e4aad7322d44019c604e0476319e076e3efdc7191cfe66e9dd606a886fd0761e83c8e4b8b71a4e4a08e59b95798d4e0bb4d877dfcf0e850262c6bbace', N'L16 Blk 32 Quezon City', N'09171234567', NULL, CAST(N'2026-07-30T17:45:21.233' AS DateTime), NULL, 1)
INSERT [dbo].[Users] ([UserID], [Username], [PasswordHash], [Address], [ContactNumber], [ImageURL], [CreatedAt], [UpdatedAt], [IsActive]) VALUES (2, N'ana', N'scrypt:32768:8:1$FJPXKlkfbj2ZUGNZ$3b6374ef7b8fa9dbb8b61a96d51d3939826d1c99037f2eec31d69eb8a0402d81c0be22ccb7b550962a33264a3d008adb1ca9c3e6fe09043c412c1243172c570a', N'22 Rizal St Manila', N'09182345678', NULL, CAST(N'2026-07-30T17:45:21.233' AS DateTime), NULL, 1)
INSERT [dbo].[Users] ([UserID], [Username], [PasswordHash], [Address], [ContactNumber], [ImageURL], [CreatedAt], [UpdatedAt], [IsActive]) VALUES (3, N'pedro', N'scrypt:32768:8:1$u7CpXsrHhWgbfgJ5$81686c6beb01f786c3dc25d18aa067139e0c76b0e7478b67a50fe1040f95ef346e681549971ea6617d4d3893f26b5e78dba4230be34e02150027c6b10f188a4c', N'5 Mabini Ave Cavite', N'09193456789', NULL, CAST(N'2026-07-30T17:45:21.233' AS DateTime), NULL, 1)
INSERT [dbo].[Users] ([UserID], [Username], [PasswordHash], [Address], [ContactNumber], [ImageURL], [CreatedAt], [UpdatedAt], [IsActive]) VALUES (4, N'maria', N'scrypt:32768:8:1$Tu0cJvf3O3A9Njd5$bf244b3994d13ca775ea6e07bfee017ba3a842ef19b90e29a1ec3698bb2c1a3991a4a432db72bef6eecfb7638a68e02ad09739c8aea807e9d8bf901531b22fab', N'88 Luna St Laguna', N'09204567890', NULL, CAST(N'2026-07-30T17:45:21.233' AS DateTime), NULL, 1)
INSERT [dbo].[Users] ([UserID], [Username], [PasswordHash], [Address], [ContactNumber], [ImageURL], [CreatedAt], [UpdatedAt], [IsActive]) VALUES (5, N'jose', N'scrypt:32768:8:1$Ki5wWDZnEE2q9uZo$7e5ba5588e4faf540fb5531fd2f22dde4ca038cc64e1d414810641f7a9d71884d360f54820cbf821d1760927c214bec33bf7063fda2f5f8deb310c0af471936b', N'12 Aguinaldo Batangas', N'09215678901', NULL, CAST(N'2026-07-30T17:45:21.233' AS DateTime), NULL, 1)
INSERT [dbo].[Users] ([UserID], [Username], [PasswordHash], [Address], [ContactNumber], [ImageURL], [CreatedAt], [UpdatedAt], [IsActive]) VALUES (6, N'carla', N'scrypt:32768:8:1$qF0xX1P7xUWPXwMj$c07f0fabd904fe0199b808613442904e05e7a0aa1c02e6a6454e892d22108fab2a8d9555ecfdeb6e1cb2bf3cbc2092663580ba70e129f34128d0f55150614d51', N'9 Bonifacio Bulacan', N'09226789012', NULL, CAST(N'2026-07-30T17:45:21.233' AS DateTime), NULL, 1)
INSERT [dbo].[Users] ([UserID], [Username], [PasswordHash], [Address], [ContactNumber], [ImageURL], [CreatedAt], [UpdatedAt], [IsActive]) VALUES (7, N'mark', N'scrypt:32768:8:1$uCnmz1se55FfqEkD$e871f8711ecc6208571a584bfc048af9e21381acf72b14d633df6a4c741153866a5e16ad03c213d5dfadee11815a11ec79a48d260f2cac7c3dc99e9b9', N'3 Del Pilar Rizal', N'09237890123', NULL, CAST(N'2026-07-30T17:45:21.233' AS DateTime), NULL, 1)
INSERT [dbo].[Users] ([UserID], [Username], [PasswordHash], [Address], [ContactNumber], [ImageURL], [CreatedAt], [UpdatedAt], [IsActive]) VALUES (8, N'grace', N'scrypt:32768:8:1$CSF7EvOkBKGpY0Ss$1831d40bf67d8ebf7051bed09efedacc2ffdc9e8700fdfb0dca4e7fab261a5e5638c28fd5f831c276cdfeb78be1f9393080a6819119389ad47c4e2540d91992e', N'77 Katipunan QC', N'09248901234', NULL, CAST(N'2026-07-30T17:45:21.233' AS DateTime), NULL, 1)
INSERT [dbo].[Users] ([UserID], [Username], [PasswordHash], [Address], [ContactNumber], [ImageURL], [CreatedAt], [UpdatedAt], [IsActive]) VALUES (9, N'leo', N'scrypt:32768:8:1$J7QbxEb121fjWYt2$e3d0132809e4de576f6dd6b71962a9e348c67f2b201f9e7f9874738b1146909f453714a739b4d3e8ac10e8028b95b45c5775b5372411f51397fe885497e71da4', N'41 EDSA Makati', N'09259012345', NULL, CAST(N'2026-07-30T17:45:21.233' AS DateTime), NULL, 1)
INSERT [dbo].[Users] ([UserID], [Username], [PasswordHash], [Address], [ContactNumber], [ImageURL], [CreatedAt], [UpdatedAt], [IsActive]) VALUES (10, N'nina', N'scrypt:32768:8:1$Czw5LOW3Nk7rRnhw$559887cf73a834ac6e1d66f75d9af6da1e8d3369b72848715eb7024d312114ca913617ced6d066959ae9fae01043bae557d98feaed8cdf3139c45f04d4c315dc', N'18 Ortigas Pasig', N'09260123456', NULL, CAST(N'2026-07-30T17:45:21.233' AS DateTime), NULL, 1)
SET IDENTITY_INSERT [dbo].[Users] OFF
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_Categories]    Script Date: 30/07/2026 9:45:41 pm ******/
ALTER TABLE [dbo].[Categories] ADD  CONSTRAINT [IX_Categories] UNIQUE NONCLUSTERED 
(
	[Name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IX_ReturnForms]    Script Date: 30/07/2026 9:45:41 pm ******/
ALTER TABLE [dbo].[ReturnForms] ADD  CONSTRAINT [IX_ReturnForms] UNIQUE NONCLUSTERED 
(
	[BorrowFormID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_Users]    Script Date: 30/07/2026 9:45:41 pm ******/
ALTER TABLE [dbo].[Users] ADD  CONSTRAINT [IX_Users] UNIQUE NONCLUSTERED 
(
	[Username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
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
/****** Object:  StoredProcedure [dbo].[uspAcceptBorrowRequest]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspAcceptBorrowRequest]
	@borrow_id int,
	@item_id int
AS
BEGIN
	SET NOCOUNT ON

	DECLARE @form_status varchar(20), @item_status varchar(20)
	
	SELECT
		@form_status = [Status]
	FROM BorrowForms
	WHERE BorrowFormID = @borrow_id

	SELECT
		@item_status = [Status]
	FROM Items 
	WHERE ItemID = @item_id

	IF @item_id IS NULL
	BEGIN
		SELECT 'NOT_FOUND' AS Result
		RETURN
	END

	IF @form_status <> 'Pending'
	BEGIN
		SELECT 'NOT_PENDING' AS Result
		RETURN
	END

	IF @item_status <> 'Available'
	BEGIN
		SELECT 'ITEM_UNAVAILABLE' AS Result
		RETURN
	END

	BEGIN TRANSACTION
	BEGIN TRY
		UPDATE BorrowForms
		SET [Status] = 'Accepted', ApprovedAt = GETDATE()
		WHERE BorrowFormID = @borrow_id

		UPDATE Items
		SET [Status] = 'Borrowed', UpdatedAt = GETDATE()
		WHERE ItemID = @item_id

		UPDATE BorrowForms
		SET [Status] = 'Declined', DeclineReason = 'Item was borrowed by another user'
		WHERE ItemID = @item_id AND [Status] = 'Pending' AND BorrowFormID <> @borrow_id

		COMMIT TRANSACTION
		SELECT 'SUCCESS' AS Result
	END TRY
	BEGIN CATCH
		ROLLBACK TRANSACTION
		THROW
	END CATCH
END
GO
/****** Object:  StoredProcedure [dbo].[uspAddItem]    Script Date: 30/07/2026 9:45:41 pm ******/
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
/****** Object:  StoredProcedure [dbo].[uspBorrowItem]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspBorrowItem]
	@borrower_id int,
	@item_id int,
	@start date,
	@return date
AS
BEGIN
	SET NOCOUNT ON

	DECLARE @owner_id int, @status varchar(20), @deposit smallmoney

	SELECT @owner_id = OwnerID, @status = [Status], @deposit = SecurityDeposit
	FROM Items
	WHERE ItemID = @item_id

	IF @owner_id IS NULL
	BEGIN
		SELECT 'NOT_FOUND' AS Result
		RETURN
	END

	IF @owner_id = @borrower_id
	BEGIN
		SELECT 'OWN_ITEM' AS Result
		RETURN
	END

	IF @status <> 'Available'
	BEGIN
		SELECT 'NOT_AVAILABLE' AS Result
		RETURN
	END

	IF @start < CAST(GETDATE() AS date)
	BEGIN
		SELECT 'START_IN_PAST' AS Result
		RETURN
	END

	IF @return < @start
	BEGIN
		SELECT 'INVALID_DATES' AS Result
		RETURN;
	END

	INSERT BorrowForms (BorrowerID, ItemID, StartDate, ReturnDate, [Status], SecurityDepositSnapShot)
	VALUES (@borrower_id, @item_id, @start, @return, 'Pending', @deposit)

	SELECT 'SUCCESS' AS Result
END
GO
/****** Object:  StoredProcedure [dbo].[uspCancelBorrowRequest]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspCancelBorrowRequest]
	@id int
AS
BEGIN
	SET NOCOUNT ON;

	DECLARE @status varchar(20)

	SELECT @status = [Status]
	FROM BorrowForms
	WHERE BorrowFormID = @id 

	IF @status IS NULL
	BEGIN
		SELECT 'NOT_FOUND' AS Result
		RETURN
	END

	IF @status <> 'Pending'
	BEGIN
		SELECT 'NOT_PENDING' AS Result
		RETURN
	END

	UPDATE BorrowForms
	SET [Status] = 'Cancelled'
	WHERE BorrowFormID = @id

	SELECT 'SUCCESS' AS Result
END
GO
/****** Object:  StoredProcedure [dbo].[uspDeclineBorrowRequest]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspDeclineBorrowRequest]
	@borrow_id int,
	@owner_id int,
	@decline_reason varchar(100) = NULL
AS
BEGIN
	SET NOCOUNT ON;

	DECLARE @form_status varchar(20)

	SELECT @form_status = bf.[Status]
	FROM BorrowForms bf
		JOIN Items i ON bf.ItemID = i.ItemID
	WHERE bf.BorrowFormID = @borrow_id AND i.OwnerID = @owner_id

	IF @form_status IS NULL
	BEGIN
		SELECT 'NOT_FOUND' AS Result
		RETURN;
	END

	IF @form_status <> 'Pending'
	BEGIN
		SELECT 'NOT_PENDING' AS Result
		RETURN;
	END

	UPDATE BorrowForms
	SET [Status] = 'Declined', DeclineReason = @decline_reason
	WHERE BorrowFormID = @borrow_id

	SELECT 'SUCCESS' AS Result
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetAllCommunityItems]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetAllCommunityItems]
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
		, CASE
			WHEN i.[Status] = 'Borrowed' THEN 'Borrowed until ' + dbo.fnFormatDate(bf.ReturnDate)
			ELSE i.[Status]
		END AS [Status]	
	FROM Items i JOIN  Categories c
	ON i.CategoryID = c.CategoryID JOIN Users o
	ON  i.OwnerID = o.UserID LEFT JOIN BorrowForms bf
	ON i.ItemID = bf.ItemID AND bf.[Status] = 'Accepted'
	WHERE OwnerID <> @user_id AND i.[Status] <> 'Unavailable'
	ORDER BY i.CreatedAt DESC
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetApplianceCommunityItems]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetApplianceCommunityItems]
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
		, CASE
            WHEN i.[Status] = 'Borrowed' THEN 'Borrowed until ' + dbo.fnFormatDate(bf.ReturnDate)
            ELSE i.[Status]
        END AS [Status]	
	FROM Items i JOIN  Categories c
	ON i.CategoryID = c.CategoryID JOIN Users o
	ON  i.OwnerID = o.UserID LEFT JOIN BorrowForms bf
	ON i.ItemID = bf.ItemID AND bf.[Status] = 'Accepted'
	WHERE OwnerID <> @user_id AND i.[Status] <> 'Unavailable' AND c.[Name] = 'Appliance'
	ORDER BY i.CreatedAt DESC
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetBorrowRequest]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetBorrowRequest]
	@user_id int
AS
BEGIN
	SELECT 
		bf.BorrowFormID
		, i.ItemID
		, i.ImageURL
		, i.Name
		, c.Name
		, FORMAT(bf.StartDate, 'MMMM dd, yyyy')
		, FORMAT(bf.ReturnDate, 'MMMM dd, yyyy')
		, bf.SecurityDepositSnapShot
		, b.Username
	FROM BorrowForms bf JOIN Items i
	ON bf.ItemID  = i.ItemID JOIN Categories c
	ON i.CategoryID  = c.CategoryID JOIN Users o
	ON i.OwnerID = o.UserID JOIN  Users b
	ON  bf.BorrowerID = b.UserID
	WHERE o.UserID = @user_id AND bf.[Status] = 'Pending'
	AND i.Status = 'Available'
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetHistory]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetHistory]
    @user_id int
AS
BEGIN
    SELECT
        i.ImageURL,
        i.Name,
        c.Name,
        i.Condition,
        bf.StartDate,
        bf.ReturnDate,
        bf.SecurityDepositSnapShot
    FROM BorrowForms bf
    JOIN Items i ON bf.ItemID = i.ItemID
    JOIN Categories c ON i.CategoryID = c.CategoryID
    WHERE bf.BorrowerID = @user_id AND bf.Status = 'Returned';
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetItemByID]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetItemByID]
	@item_id int
AS
BEGIN
	SELECT
		i.ItemID
		, i.[Name] as ItemName
		, c.[Name] as CategoryName
		, i.Condition
		, o.Username
		, i.ImageURL
		, i.SecurityDeposit
		, i.[Status]
		, i.Note
	FROM Items i JOIN Categories c
	ON i.CategoryID = c.CategoryID JOIN Users o
	ON i.OwnerID = o.UserID
	WHERE ItemID = @item_id
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetItemByIdMyItems]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetItemByIdMyItems]
	@itemID int,
	@ownerID int
AS
BEGIN
	SET NOCOUNT ON

	SELECT
		ItemID
		, [Name]
		, CategoryID
		, Condition
		, [Description]
		, Note
		, ImageURL
		, SecurityDeposit
		, [Status]
	FROM Items
	WHERE ItemID = @itemID
	AND OwnerID = @ownerID
	AND [Status] <> 'Unavailable'
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetLatestItems]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC  [dbo].[uspGetLatestItems]
	@user_id int
AS
BEGIN
	SET NOCOUNT ON
	
	SELECT TOP 4  
		i.ItemID
		, i.ImageURL
		, i.[Name] as ItemName
		, c.[Name] as CategoryName
		, i.Condition
		, o.Username
		, i.SecurityDeposit
		, CASE
			WHEN i.[Status] = 'Borrowed' THEN 'Borrowed until ' + dbo.fnFormatDate(bf.ReturnDate)
			ELSE i.[Status]
		END AS [Status]
	FROM Items i JOIN  Categories c
	ON i.CategoryID = c.CategoryID JOIN Users o
	ON i.OwnerID = o.UserID LEFT JOIN BorrowForms bf
	ON i.ItemID = bf.ItemID AND bf.[Status] = 'Accepted'
	WHERE OwnerID <> @user_id AND i.[Status] <> 'Unavailable'
	ORDER BY i.CreatedAt DESC
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetMyBorrowRequest]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetMyBorrowRequest]
	@user_id int
AS
BEGIN
	SELECT
		bf.BorrowFormID
		, i.ImageURL
		, i.[Name]
		, c.[Name]
		, i.Condition
		, bf.StartDate
		, bf.ReturnDate
		, bf.SecurityDepositSnapShot
		, bf.[Status]
	FROM BorrowForms bf JOIN Items i
	ON bf.ItemID = i.ItemID JOIN Users o
	ON i.OwnerID = o.UserID JOIN Categories c
	ON i.CategoryID = c.CategoryID
	WHERE bf.BorrowerID = @user_id AND bf.[Status] <> 'Cancelled'
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetOnGoingBorrowedItems]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetOnGoingBorrowedItems]
	@user_id int
AS
BEGIN
	SELECT
		i.ImageURL
		, i.Name
		, c.Name
		, i.Condition
		, bf.ReturnDate
		, bf.StartDate
		, bf.SecurityDepositSnapShot
		, dbo.fnGetOnGoingRequestStatus(bf.ReturnDate) as [Status]
	FROM BorrowForms bf JOIN Items i
	ON bf.ItemID = i.ItemID JOIN Categories c
	ON i.CategoryID = c.CategoryID
	WHERE bf.BorrowerID = @user_id AND bf.Status = 'Accepted'
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetOwnerItems]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetOwnerItems]
    @ownerID int,
    @filter varchar(20) = 'all'
AS
BEGIN
    SET NOCOUNT ON

    IF @filter = 'available'
    BEGIN
        SELECT
            i.ItemID, i.ImageURL, i.[Name] AS ItemName, c.[Name] AS CategoryName,
            i.Condition, i.[Description], i.Note, i.SecurityDeposit, i.[Status], i.CreatedAt,
            bf.BorrowFormID
        FROM Items i JOIN Categories c 
		ON i.CategoryID = c.CategoryID LEFT JOIN BorrowForms bf 
		ON i.ItemID = bf.ItemID AND bf.[Status] = 'Accepted'
        WHERE i.OwnerID = @ownerID AND i.[Status] = 'Available'
        ORDER BY i.[Name]
        RETURN
    END

    IF @filter = 'borrowed'
    BEGIN
        SELECT
            i.ItemID, i.ImageURL, i.[Name] AS ItemName, c.[Name] AS CategoryName,
            i.Condition, i.[Description], i.Note, i.SecurityDeposit, i.[Status], i.CreatedAt,
            bf.BorrowFormID
        FROM Items i JOIN Categories c 
		ON i.CategoryID = c.CategoryID LEFT JOIN BorrowForms bf ON i.ItemID = bf.ItemID AND bf.[Status] = 'Accepted'
        WHERE i.OwnerID = @ownerID AND i.[Status] = 'Borrowed'
        ORDER BY i.[Name]
        RETURN
    END

    IF @filter = 'latest'
    BEGIN
        SELECT
            i.ItemID, i.ImageURL, i.[Name] AS ItemName, c.[Name] AS CategoryName,
            i.Condition, i.[Description], i.Note, i.SecurityDeposit, i.[Status], i.CreatedAt,
            bf.BorrowFormID
        FROM Items i JOIN Categories c 
		ON i.CategoryID = c.CategoryID LEFT JOIN BorrowForms bf 
		ON i.ItemID = bf.ItemID AND bf.[Status] = 'Accepted'
        WHERE i.OwnerID = @ownerID AND i.[Status] <> 'Unavailable'
        ORDER BY i.CreatedAt DESC
        RETURN
    END

    SELECT
        i.ItemID, i.ImageURL, i.[Name] AS ItemName, c.[Name] AS CategoryName,
        i.Condition, i.[Description], i.Note, i.SecurityDeposit, i.[Status], i.CreatedAt,
        bf.BorrowFormID
    FROM Items i JOIN Categories c 
	ON i.CategoryID = c.CategoryID LEFT JOIN BorrowForms bf 
	ON i.ItemID = bf.ItemID AND bf.[Status] = 'Accepted'
    WHERE i.OwnerID = @ownerID AND i.[Status] <> 'Unavailable'
    ORDER BY i.[Name]
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetReturnDetails]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetReturnDetails]
	@user_id int,
	@borrow_form int
AS
BEGIN
	SELECT
		b.ImageURL
		, b.Username
		, b.[Address]
		, i.ImageURL
		, i.Name
		, c.Name
		, i.Condition
		, bf.StartDate
		, bf.ReturnDate
		, bf.SecurityDepositSnapShot
	FROM BorrowForms bf JOIN Users b
	ON bf.BorrowerID = b.UserID JOIN Items i
	ON bf.ItemID = i.ItemID JOIN Categories c
	ON i.CategoryID = c.CategoryID JOIN Users o
	ON i.OwnerID = o.UserID
	WHERE BorrowFormID = @borrow_form AND o.UserID = @user_id
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetSearchItems]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC  [dbo].[uspGetSearchItems]
	@search varchar(100),
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
		, CASE
            WHEN i.[Status] = 'Borrowed' THEN 'Borrowed until ' + dbo.fnFormatDate(bf.ReturnDate)
            ELSE i.[Status]
        END AS [Status]		
	FROM Items i JOIN  Categories c
	ON i.CategoryID = c.CategoryID JOIN Users o
	ON i.OwnerID = o.UserID LEFT JOIN BorrowForms bf
	ON i.ItemID = bf.ItemID AND bf.[Status] = 'Accepted'
	WHERE OwnerID <> @user_id AND i.[Status] <> 'Unavailable'
	AND i.[Name] LIKE '%' + @search + '%'
	ORDER BY i.CreatedAt DESC
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetSportsCommunityItems]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetSportsCommunityItems]
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
		, CASE
            WHEN i.[Status] = 'Borrowed' THEN 'Borrowed until ' + dbo.fnFormatDate(bf.ReturnDate)
            ELSE i.[Status]
        END AS [Status]		
	FROM Items i JOIN  Categories c
	ON i.CategoryID = c.CategoryID JOIN Users o
	ON  i.OwnerID = o.UserID LEFT JOIN BorrowForms bf
	ON i.ItemID = bf.ItemID AND bf.[Status] = 'Accepted'
	WHERE OwnerID <> @user_id AND i.[Status] <> 'Unavailable' AND c.[Name] = 'Sport'
	ORDER BY i.CreatedAt DESC
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetTechnologyCommunityItems]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetTechnologyCommunityItems]
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
		, CASE
            WHEN i.[Status] = 'Borrowed' THEN 'Borrowed until ' + dbo.fnFormatDate(bf.ReturnDate)
            ELSE i.[Status]
        END AS [Status]		
	FROM Items i JOIN  Categories c
	ON i.CategoryID = c.CategoryID JOIN Users o
	ON  i.OwnerID = o.UserID LEFT JOIN BorrowForms bf
	ON i.ItemID = bf.ItemID AND bf.[Status] = 'Accepted'
	WHERE OwnerID <> @user_id AND i.[Status] <> 'Unavailable' AND c.[Name] = 'Technology'
	ORDER BY i.CreatedAt DESC
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetUserById]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetUserById]
	@user_id int
AS
BEGIN
	SELECT 
		UserID
		, Username
		, [Address]
		, ContactNumber
		, ImageURL
		, IsActive
	FROM Users
	WHERE UserID = @user_id
END
GO
/****** Object:  StoredProcedure [dbo].[uspGetUserStats]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspGetUserStats]
    @user_id int
AS
BEGIN
    SELECT
        (SELECT COUNT(*) FROM Items WHERE OwnerID = @user_id) AS ItemsShared,

        (SELECT COUNT(*)
         FROM BorrowForms bf JOIN Items i 
		 ON bf.ItemID = i.ItemID
         WHERE i.OwnerID = @user_id AND bf.Status = 'Accepted') AS ItemsLentOut,

        (SELECT COUNT(*)
         FROM BorrowForms
         WHERE BorrowerID = @user_id AND Status = 'Accepted') AS ItemsBorrowing,

        (SELECT COUNT(*)
         FROM BorrowForms
         WHERE BorrowerID = @user_id AND Status = 'Returned') AS BorrowsCompleted;
END
GO
/****** Object:  StoredProcedure [dbo].[uspLoadCategories]    Script Date: 30/07/2026 9:45:41 pm ******/
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
/****** Object:  StoredProcedure [dbo].[uspLoadCommunityItems]    Script Date: 30/07/2026 9:45:41 pm ******/
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
		,  CASE
            WHEN i.[Status] = 'Borrowed' THEN 'Borrowed until ' + dbo.fnFormatDate(bf.ReturnDate)
            ELSE i.[Status]
        END AS [Status]
	FROM Items i JOIN  Categories c
	ON i.CategoryID = c.CategoryID JOIN Users o
	ON i.OwnerID = o.UserID LEFT  JOIN BorrowForms bf
	ON i.ItemID = bf.ItemID AND bf.[Status] = 'Accepted'
	WHERE OwnerID <> @user_id AND i.[Status] <> 'Unavailable'
END
GO
/****** Object:  StoredProcedure [dbo].[uspLoginUser]    Script Date: 30/07/2026 9:45:41 pm ******/
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
/****** Object:  StoredProcedure [dbo].[uspRegisterUser]    Script Date: 30/07/2026 9:45:41 pm ******/
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
/****** Object:  StoredProcedure [dbo].[uspReturnItem]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspReturnItem]
    @user_id int,          
    @borrow_form int,
    @actual_return date,
    @damage_fee smallmoney
AS
BEGIN
    SET NOCOUNT ON

    DECLARE @item_id int, @owner_id int, @status varchar(20), 
	@expected_return date,  @penalty smallmoney

    SELECT
        @item_id = bf.ItemID,
        @status = bf.[Status],
        @expected_return = bf.ReturnDate,
        @owner_id = i.OwnerID
    FROM BorrowForms bf
    JOIN Items i ON bf.ItemID = i.ItemID
    WHERE bf.BorrowFormID = @borrow_form;

    IF @item_id IS NULL
    BEGIN
        SELECT 'NOT_FOUND' AS Result
        RETURN
    END

    IF @owner_id <> @user_id
    BEGIN
        SELECT 'NOT_OWNER' AS Result
        RETURN
    END

    IF @status <> 'Accepted'
    BEGIN
        SELECT 'NOT_ACTIVE' AS Result
        RETURN
    END

    IF @damage_fee IS NULL OR @damage_fee < 0
    BEGIN
        SELECT 'INVALID_DAMAGE' AS Result
        RETURN
    END

	SET @penalty = dbo.fnCalculateLatePenalty(@expected_return, @actual_return)

    INSERT INTO ReturnForms (BorrowFormID, ActualReturnDate, DamageFee, LatePenalty)
    VALUES (@borrow_form, @actual_return, @damage_fee, @penalty)

	UPDATE BorrowForms 
	SET [Status] = 'Returned' 
	WHERE BorrowFormID = @borrow_form

    UPDATE Items 
	SET [Status] = 'Available', UpdatedAt = GETDATE()
	WHERE ItemID = @item_id

    SELECT 'SUCCESS' AS Result
END
GO
/****** Object:  StoredProcedure [dbo].[uspSearchItems]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspSearchItems]
    @ownerID int,
    @search varchar(100),
    @filter varchar(20) = 'all'
AS
BEGIN
    SET NOCOUNT ON

    SELECT
        i.ItemID, i.ImageURL, i.[Name] AS ItemName, c.[Name] AS CategoryName,
        i.Condition, i.[Description], i.Note, i.SecurityDeposit, i.[Status], i.CreatedAt,
        bf.BorrowFormID
    FROM Items i
    JOIN Categories c ON i.CategoryID = c.CategoryID
    LEFT JOIN BorrowForms bf ON i.ItemID = bf.ItemID AND bf.[Status] = 'Accepted'
    WHERE i.OwnerID = @ownerID
    AND i.[Status] <> 'Unavailable'
    AND (
        @filter = 'all' OR @filter = 'latest'
        OR (@filter = 'available' AND i.[Status] = 'Available')
        OR (@filter = 'borrowed' AND i.[Status] = 'Borrowed')
    )
    AND (
        i.[Name] LIKE '%' + @search + '%'
        OR c.[Name] LIKE '%' + @search + '%'
        OR i.Condition LIKE '%' + @search + '%'
        OR ISNULL(i.[Description], '') LIKE '%' + @search + '%'
        OR ISNULL(i.Note, '') LIKE '%' + @search + '%'
    )
    ORDER BY
        CASE WHEN @filter = 'latest' THEN i.CreatedAt END DESC,
        CASE WHEN @filter <> 'latest' THEN i.[Name] END ASC
END

GO
/****** Object:  StoredProcedure [dbo].[uspUpdateItem]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspUpdateItem]
	@itemID int,
	@ownerID int,
	@name varchar(100),
	@category int,
	@condition varchar(50),
	@description varchar(255),
	@note varchar(255),
	@image varchar(255),
	@securityDeposit smallmoney
AS
BEGIN
	SET NOCOUNT ON

	IF NOT EXISTS (
		SELECT 1
		FROM Items
		WHERE ItemID = @itemID
		AND OwnerID = @ownerID
		AND [Status] <> 'Unavailable'
	)
	BEGIN
		SELECT 'ITEM NOT FOUND' AS Result
		RETURN
	END

	IF EXISTS (
		SELECT 1
		FROM Items
		WHERE ItemID = @itemID
		AND OwnerID = @ownerID
		AND [Status] = 'Borrowed'
	)
	BEGIN
		SELECT 'ITEM BORROWED' AS Result
		RETURN
	END

	IF @name IS NULL OR LTRIM(RTRIM(@name)) = ''
	BEGIN
		SELECT 'NO NAME' AS Result
		RETURN
	END

	IF @category IS NULL
	BEGIN
		SELECT 'NO CATEGORY' AS Result
		RETURN
	END

	IF NOT EXISTS (
		SELECT 1
		FROM Categories
		WHERE CategoryID = @category
		AND IsActive = 1
	)
	BEGIN
		SELECT 'INVALID CATEGORY' AS Result
		RETURN
	END

	IF @condition IS NULL OR LTRIM(RTRIM(@condition)) = ''
	BEGIN
		SELECT 'NO CONDITION' AS Result
		RETURN
	END

	IF @securityDeposit IS NULL OR @securityDeposit < 0
	BEGIN
		SELECT 'INVALID DEPOSIT' AS Result
		RETURN
	END

	UPDATE Items
	SET [Name] = @name
		, CategoryID = @category
		, Condition = @condition
		, [Description] = @description
		, Note = @note
		, ImageURL = COALESCE(@image, ImageURL)
		, SecurityDeposit = @securityDeposit
		, UpdatedAt = GETDATE()
	WHERE ItemID = @itemID
	AND OwnerID = @ownerID

	SELECT 'SUCCESS' AS Result
END
GO
/****** Object:  StoredProcedure [dbo].[uspUpdateItemStatus]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspUpdateItemStatus]
	@itemID int,
	@ownerID int,
	@status varchar(20)
AS
BEGIN
	SET NOCOUNT ON

	IF NOT EXISTS (
		SELECT 1
		FROM Items
		WHERE ItemID = @itemID
		AND OwnerID = @ownerID
	)
	BEGIN
		SELECT 'ITEM NOT FOUND' AS Result
		RETURN
	END

	IF EXISTS (
		SELECT 1
		FROM Items
		WHERE ItemID = @itemID
		AND OwnerID = @ownerID
		AND [Status] = 'Borrowed'
	)
	AND @status = 'Unavailable'
	BEGIN
		SELECT 'ITEM BORROWED' AS Result
		RETURN
	END

	IF EXISTS (
		SELECT 1
		FROM Items
		WHERE ItemID = @itemID
		AND OwnerID = @ownerID
		AND [Status] = 'Unavailable'
	)
	BEGIN
		SELECT 'ALREADY UNAVAILABLE' AS Result
		RETURN
	END

	UPDATE Items
	SET [Status] = @status
		, UpdatedAt = GETDATE()
	WHERE ItemID = @itemID
	AND OwnerID = @ownerID

	SELECT 'SUCCESS' AS Result
END
GO
/****** Object:  StoredProcedure [dbo].[uspUpdateUser]    Script Date: 30/07/2026 9:45:41 pm ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROC [dbo].[uspUpdateUser]
	@user_id int,
	@username varchar(100),
	@address varchar(150),
	@contact varchar(20),
	@image varchar(255)
AS
BEGIN

	SET NOCOUNT ON

	IF EXISTS (SELECT 1 FROM Users WHERE Username = @username AND UserID <> @user_id)
	BEGIN
		SELECT 'USERNAME_TAKEN' AS Result
		RETURN
	END

	UPDATE Users
	SET Username = @username, Address = @address, ContactNumber = @contact, 
	ImageURL = COALESCE(@image, ImageURL), UpdatedAt = GETDATE()
	WHERE UserID = @user_id

	SELECT 'SUCCESS' AS Result
END
GO
USE [master]
GO
ALTER DATABASE [INFODBM_FINALS] SET  READ_WRITE 
GO
