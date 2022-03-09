import 'package:test/test.dart';
import 'package:flutter_application_5/models/plant_post.dart';

void main() {
  test('data created from json should have appropriate values', () {
    const date = '2022-03-03';
    const url = 'testurl';
    const quantity = '5';
    const latitude = '1.0';
    const longitude = '2.0';

    final plantPost = PlantPost.fromJSON({
      'date': date,
      'photoUrl': url,
      'itemCount': quantity.toString(),
      'latitude': latitude,
      'longitude': longitude
    });

    expect(plantPost.date, DateTime.parse(date));
    expect(plantPost.photoUrl, url);
    expect(plantPost.itemCount, int.parse(quantity));
    expect(plantPost.latitude, double.parse(latitude));
    expect(plantPost.longitude, double.parse(longitude));
  });

  test('PlantPost object successfully created', () {
    final date = DateTime.parse('2022-03-03');
    const url = 'testurl';
    const quantity = 5;
    const latitude = 1.0;
    const longitude = 2.0;

    PlantPost testPost = PlantPost(
        date: date,
        photoUrl: url,
        itemCount: quantity,
        latitude: latitude,
        longitude: longitude);

    expect(testPost, isA<PlantPost>());
  });
}
