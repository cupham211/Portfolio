import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:flutter_application_5/models/plant_post.dart';

class DetailPost extends StatelessWidget {
  static const routeName = "DetailScreen";

  const DetailPost({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final entry = ModalRoute.of(context)!.settings.arguments as PlantPost;
    final DateFormat formatter = DateFormat.yMMMMd('en_US');

    return Scaffold(
        appBar: AppBar(
            leading: Builder(builder: (BuildContext context) {
              return Semantics(
                button: true,
                enabled: true,
                onTapHint: 'Return to previous screen',
                child: IconButton(
                  icon: const Icon(Icons.arrow_back_ios_new_rounded),
                  onPressed: () {
                    Navigator.of(context).pop();
                  }));
            }),
            title: const Text('Plantstagram'),
            centerTitle: true,),
        body: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            Semantics(
              label: 'date item was added',
              child: Text(formatter.format(entry.date),
                style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w500))),
            Semantics(
              image: true,
              label: 'A beautiful photo of a plant',
              child: Image.network(entry.photoUrl, fit: BoxFit.scaleDown)),
            Semantics(
              label: 'number of plants in photo that is owned',
              child: Text('Items: ${entry.itemCount}',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w400))),
            Semantics(
              label: 'the geolocation the photo was taken',
              readOnly: true,
              child: Text('${entry.latitude}, ${entry.longitude}',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w400)))
          ],
        ));
  }
}
