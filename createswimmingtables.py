#!/usr/bin/python

import psycopg2
from config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE logins (
            ID SERIAL PRIMARY KEY,
            UserName VARCHAR(255) NOT NULL,
            PasswordSalt VARCHAR(255),
            PasswordHash VARCHAR(255),
            RelatedUserID VARCHAR(255)
        )
        """,
        """
        CREATE TABLE users (
            ID SERIAL PRIMARY KEY,
            FirstName VARCHAR(255) NOT NULL,
            LastName VARCHAR(255) NOT NULL,
            UserName VARCHAR(255) NOT NULL,
            Email VARCHAR(255),
            Phone VARCHAR(255),
            Mobile VARCHAR(255),
            DOB VARCHAR(255),
            RegDate VARCHAR(255)
                )
                """,

        """
        CREATE TABLE memberships (
            ID SERIAL PRIMARY KEY,
            UserID VARCHAR(255) NOT NULL,
            CompanyID VARCHAR(255),
            RoleID VARCHAR(255),
            Email VARCHAR(255),
            Phone VARCHAR(255),
            Mobile VARCHAR(255),
            DOB VARCHAR(255),
            RegDate VARCHAR(255)
               )
               """,
        """
               CREATE TABLE regswimmer (
                   ID SERIAL PRIMARY KEY,
                   UserID VARCHAR(255) NOT NULL,
                   FirstName VARCHAR(255) NOT NULL,
                   LastName VARCHAR(255) NOT NULL,
                   Address VARCHAR(255),
                   Postcode VARCHAR(10),
                   DOB date,
                   Gender VARCHAR(10),
                   Phone1 VARCHAR(20),
                   Phone2 VARCHAR(20),
                   Email VARCHAR(255),
                   MedicalCondition char(3),
                   MedicalCondDetails VARCHAR(255),
                   MemberOfClub char(1),
                   NameOfClub VARCHAR(255),
                   LengthOfTime VARCHAR(55),
                   DataProtectConsent char(3),
                   MembershipConsent char(3),
                   RegDate VARCHAR(255)
                   )
                      """,

        """
        CREATE TABLE companies (
            ID SERIAL PRIMARY KEY,
            Name VARCHAR(255) NOT NULL,
            AccessLevel VARCHAR(255),
            AccountID VARCHAR(255)
                )
                """,

        """
        CREATE TABLE accounts (
            ID SERIAL PRIMARY KEY,
            Name VARCHAR(255),
            PlanLevel VARCHAR(255)
                )
                """,
        """
        CREATE TABLE swimrecords (
            ID SERIAL PRIMARY KEY,
            UserID VARCHAR(255) NOT NULL,
            EventID VARCHAR(255),
            CompanyID VARCHAR(255),
            Stroke VARCHAR(255),
            Date VARCHAR(255),
            Event VARCHAR(255),
            TimeMins bigint,
            TimeSecs bigint,
            TimeMilliSecs bigint,
            Comments VARCHAR(255),
            AwardID VARCHAR(255),
            ClubPoint bigint,
            Status VARCHAR(255)
                )
                """,

        """
        CREATE TABLE payments (
            ID SERIAL PRIMARY KEY,
            UserID VARCHAR(255) NOT NULL,
            EventID VARCHAR(255),
            MembershipFees numeric(5,2),
            FeesPaid numeric(5,2),
            TaxesPaid numeric(5,2),
            EventFees numeric(5,2),
            GalaFees numeric(5,2),
            TransportCost numeric(5,2),
            Comments VARCHAR(255),
            Status VARCHAR(255)
                       )
                       """,

        """
    CREATE TABLE events (
        ID SERIAL PRIMARY KEY,
        EventName VARCHAR(255) NOT NULL,
        EventID VARCHAR(255),
        EventDate date,
        Status VARCHAR(255)
        )
        """,

        """
    CREATE TABLE awards (
        ID SERIAL PRIMARY KEY,
        AwardName VARCHAR(255),
        Comments VARCHAR(255)
        )
        """,
)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()