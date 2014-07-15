create table songs (
  id integer primary key autoincrement,
  base64name varchar not null,
  songname varchar not null,
  dateconverted date not null,
  timesdownloaded integer null,
  lastdownload date null

);
