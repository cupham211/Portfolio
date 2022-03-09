//import 'dart:html';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:location/location.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
//import 'package:firebase_storage/firebase_storage.dart';
import 'package:flutter_application_5/screens/plant_list_screen.dart';

class NewPost extends StatefulWidget {
  static const routeName = 'NewEntry';

  const NewPost({Key? key}) : super(key: key);

  @override
  _NewPostState createState() => _NewPostState();
}

class _NewPostState extends State<NewPost> {
  Map url = {};
  LocationData? locationData;
  var locationService = Location();

  @override
  void initState() {
    super.initState();
    retrieveLocation();
  }

  void retrieveLocation() async {
    try {
      var _serviceEnabled = await locationService.serviceEnabled();
      if (!_serviceEnabled) {
        _serviceEnabled = await locationService.requestService();
        if (!_serviceEnabled) {
          // ignore: avoid_print
          print('Failed to enable service. Returning.');
          return;
        }
      }

      var _permissionGranted = await locationService.hasPermission();
      if (_permissionGranted == PermissionStatus.denied) {
        _permissionGranted = await locationService.requestPermission();
        if (_permissionGranted != PermissionStatus.granted) {
          // ignore: avoid_print
          print('Location service permission not granted. Returning.');
        }
      }

      locationData = await locationService.getLocation();
    } on PlatformException catch (e) {
      // ignore: avoid_print
      print('Error: ${e.toString()}, code: ${e.code}');
      locationData = null;
    }
    locationData = await locationService.getLocation();
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    url = ModalRoute.of(context)!.settings.arguments as Map;
    final formKey = GlobalKey<FormState>();
    int numItems = 0;
    return Scaffold(
        appBar: AppBar(
          leading: Builder(builder: (BuildContext context) {
            return Semantics(
              button: true,
              enabled: true,
              onTapHint: 'Return to plant list screen',
              child: IconButton(
                icon: const Icon(Icons.arrow_back_ios_new_rounded),
                onPressed: () {
                  Navigator.pop(context);
                }));
          }),
          title: const Text('Plantstagram'),
          centerTitle: true,
        ),
        resizeToAvoidBottomInset: false,
        body: SingleChildScrollView(
            child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
              Semantics(
                image: true,
                label: 'the beautiful photo of a plant selected',
                child: Image.network(url['urlLink'].toString(), fit: BoxFit.scaleDown)),
              Form(
                  key: formKey,
                  child: Column(children: [
                    Padding(
                        padding: const EdgeInsets.only(top: 20),
                        child: Semantics(
                          textField: true,
                          enabled: true,
                          label: 'Please enter number of plants in photo that is owned.',
                          child: TextFormField(
                            autofocus: true,
                            decoration: const InputDecoration(
                                labelText: 'Number of Plants',
                                border: OutlineInputBorder()),
                            onSaved: (value) {
                              numItems = int.parse(value!);
                            },
                            validator: (value) {
                              if (value!.isEmpty) {
                                return 'Please enter an amount';
                              } else if (int.parse(value) % 1 != 0) {
                                return 'Please enter a whole number';
                              }
                              return null;
                            }))),
                        const SizedBox(height: 25.0,),    
                    Align(
                        alignment: Alignment.bottomCenter,
                        child: Semantics(
                          button: true,
                          enabled: true,
                          onTapHint: "save the plant information into the app database",
                          child: ElevatedButton(
                          style: ElevatedButton.styleFrom(
                              minimumSize:
                                  const Size(400, 100)),
                          onPressed: () {
                            if (formKey.currentState!.validate()) {
                              formKey.currentState!.save();
                              uploadData(numItems);
                              Navigator.pushReplacementNamed(
                                  context, CameraScreen.routeName);
                            }
                          },
                          child: const Icon(Icons.cloud_upload_outlined),
                        )))
                  ])),

            ])));
  }

  // void uploadData(ImageSource source) async {
  //   final url = await getImage(source);
  void uploadData(numItems) {
    final urlLink = url['urlLink'];
    final date = Timestamp.fromDate(DateTime.now());
    final count = numItems;
    final latitude = locationData!.latitude;
    final longitude = locationData!.longitude;
    FirebaseFirestore.instance.collection('posts').add({
      'date': date,
      'itemCount': count,
      'photoUrl': urlLink,
      'latitude': latitude,
      'longitude': longitude
    });
  }
}
