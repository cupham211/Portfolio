const Express = require("express");
const BodyParser = require("body-parser");
const Mongoose = require('mongoose');

const app = Express();
const dbURL = "mongodb://localhost:27017/plantwatchDB"

Mongoose.connect(dbURL);
const db = Mongoose.connection

db.once('open', _ => {
  console.log('Database connected:', dbURL)
});
db.on('error', err => {
  console.error('connection error:', err)
});

app.use(BodyParser.json());
app.use(BodyParser.urlencoded({
  extended: true
}));

const bayEntry = Mongoose.model('bayarea', {
  area: String,
  store: String,
  address: String,
  website: String,
  restock_day: String
});

app.post("/", async (req, res, next) => {
  try {
    var entry = new bayEntry(req.body);
    var result = await entry.save();
    res.send(result);
  } catch (error) {
      res.status(500).send(error);
  }
});

app.get("/", async (req, res, next) => {
  try {
    var result = await bayEntry.find(req.query).exec();
    res.send(result);
  } catch (error) {
      res.status(500).send(error);
  }
});

app.put("/:id", async (req, res, next) => {
  try {
    var update = await bayEntry.findById(req.params.id).exec();
    update.set(req.body);
    var result = await update.save();
    res.send(result);
  } catch (error) {
      res.status(500).send(error);
  }
});

app.delete("/:id", async (req, res, next) => {
  try {
    var result = await bayEntry.deleteOne({
      _id: req.params.id
    }).exec();
    res.send(result);
  } catch (error) {
      res.status(500).send(error);
  }
});

app.listen(3000, function() {
  console.log("server started on port 3000")
});
