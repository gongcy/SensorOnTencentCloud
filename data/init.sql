CREATE TABLE "sensordata" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"utime" INTEGER NOT NULL,
"utype" INTEGER DEFAULT 0 NOT NULL,
"udata" REAL NOT NULL,
"sdata" TEXT
);
