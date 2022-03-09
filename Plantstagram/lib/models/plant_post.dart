
class PlantPost {
  //photo, date, number of items, and latitude/longitude
  final String photoUrl;
  final DateTime date;
  final int itemCount;
  final double latitude;
  final double longitude;
  

  PlantPost(
      {required this.photoUrl,
      required this.date,
      required this.itemCount,
      required this.latitude,
      required this.longitude});

  factory PlantPost.fromJSON(Map<String, dynamic> json) {
    return PlantPost(
        date: DateTime.parse(json['date']),
        photoUrl: json['photoUrl'],
        itemCount: int.parse(json['itemCount']),
        latitude: double.parse(json['latitude']),
        longitude: double.parse(json['longitude']));
  }
}
