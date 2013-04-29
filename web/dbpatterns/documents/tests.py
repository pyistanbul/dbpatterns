import os
import json

from django.test import TestCase

from documents.models import Document
from documents.exporters.sql import (MysqlExporter, OracleExporter,
                                     PostgresExporter, SQLiteExporter)


TEST_DOCUMENT_PATH = os.path.join(os.path.dirname(__file__),
                                  "fixtures/test_document.json")


class ExporterTestCase(TestCase):
    def setUp(self):
        self.document = Document(json.load(open(TEST_DOCUMENT_PATH)))

    def test_mysql_exporter(self):
        """
        Tests MySQL exporter.
        """
        exporter = MysqlExporter(self.document)
        self.assertEqual(exporter.as_text(), """
CREATE TABLE `permissions` (
	`id` int PRIMARY KEY,
	`name` varchar(255)
);
CREATE TABLE `users_roles` (
	`users_id` int,
	`roles_id` int,
	FOREIGN KEY(`users_id`) REFERENCES `users` (`id`),
	FOREIGN KEY(`roles_id`) REFERENCES `roles` (`id`)
);
CREATE TABLE `roles` (
	`id` int PRIMARY KEY,
	`name` varchar(255)
);
CREATE TABLE `roles_permissions` (
	`roles_id` int,
	`permissions_id` int,
	FOREIGN KEY(`roles_id`) REFERENCES `roles` (`id`),
	FOREIGN KEY(`permissions_id`) REFERENCES `permissions` (`id`)
);
CREATE TABLE `users` (
	`id` int PRIMARY KEY,
	`name` varchar(255)
);""".strip())


    def test_oracle_exporter(self):
        """
        Tests Oracle exporter.
        """
        exporter = OracleExporter(self.document)
        self.assertEqual(exporter.as_text(), """
CREATE TABLE "permissions" (
	"id" int PRIMARY KEY,
	"name" varchar(255)
);
CREATE TABLE "users_roles" (
	"users_id" int CONSTRAINT users_id REFERENCES users(id),
	"roles_id" int CONSTRAINT roles_id REFERENCES roles(id)
);
CREATE TABLE "roles" (
	"id" int PRIMARY KEY,
	"name" varchar(255)
);
CREATE TABLE "roles_permissions" (
	"roles_id" int CONSTRAINT roles_id REFERENCES roles(id),
	"permissions_id" int CONSTRAINT permissions_id REFERENCES permissions(id)
);
CREATE TABLE "users" (
	"id" int PRIMARY KEY,
	"name" varchar(255)
);""".strip())


    def test_postgres_exporter(self):
        """
        Tests Postgres exporter.
        """
        exporter = PostgresExporter(self.document)
        self.assertEqual(exporter.as_text(), """
CREATE TABLE "permissions" (
	"id" int PRIMARY KEY,
	"name" varchar(255)
);
CREATE TABLE "users_roles" (
	"users_id" int,
	"roles_id" int,
	FOREIGN KEY("users_id") REFERENCES "users" ("id"),
	FOREIGN KEY("roles_id") REFERENCES "roles" ("id")
);
CREATE TABLE "roles" (
	"id" int PRIMARY KEY,
	"name" varchar(255)
);
CREATE TABLE "roles_permissions" (
	"roles_id" int,
	"permissions_id" int,
	FOREIGN KEY("roles_id") REFERENCES "roles" ("id"),
	FOREIGN KEY("permissions_id") REFERENCES "permissions" ("id")
);
CREATE TABLE "users" (
	"id" int PRIMARY KEY,
	"name" varchar(255)
);""".strip())


    def test_sqlite_exporter(self):
        """
        Tests SQLite exporter.
        """
        exporter = SQLiteExporter(self.document)
        self.assertEqual(exporter.as_text(), """
CREATE TABLE "permissions" (
	"id" int PRIMARY KEY,
	"name" varchar(255)
);
CREATE TABLE "users_roles" (
	"users_id" int FOREIGN KEY("users_id") REFERENCES "users" ("id"),
	"roles_id" int FOREIGN KEY("roles_id") REFERENCES "roles" ("id")
);
CREATE TABLE "roles" (
	"id" int PRIMARY KEY,
	"name" varchar(255)
);
CREATE TABLE "roles_permissions" (
	"roles_id" int FOREIGN KEY("roles_id") REFERENCES "roles" ("id"),
	"permissions_id" int FOREIGN KEY("permissions_id") REFERENCES "permissions" ("id")
);
CREATE TABLE "users" (
	"id" int PRIMARY KEY,
	"name" varchar(255)
);""".strip())