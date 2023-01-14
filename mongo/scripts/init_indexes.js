db = db.getSiblingDB('data');

db.createCollection('titles');
db.titles.createIndex({
  name: "text",
})
db.createCollection('actors');
db.actors.createIndex({
  name: "text",
})
// db.titles.createIndex({
//   cast: "text"
// })