import 'dart:io';
//import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:image_picker/image_picker.dart';
import 'package:flutter_application_5/models/plant_post.dart';
import 'package:flutter_application_5/screens/new_plant_screen.dart';
import 'package:flutter_application_5/screens/plant_detail_screen.dart';

class CameraScreen extends StatefulWidget {
  static const routeName = 'CameraScreen';

  const CameraScreen({Key? key}) : super(key: key);

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  File? image;
  final picker = ImagePicker();

/*
* Pick an image from the gallery, upload it to Firebase Storage and return 
* the URL of the image in Firebase Storage.
*/
  Future getImage(ImageSource source) async {
    final pickedFile = await picker.pickImage(source: source);
    image = File(pickedFile!.path);

    var fileName = DateTime.now().toString() + '.jpg';
    Reference storageReference = FirebaseStorage.instance.ref().child(fileName);
    UploadTask uploadTask = storageReference.putFile(image!);
    await uploadTask;
    final url = await storageReference.getDownloadURL();
    return url;
  }

  @override
  Widget build(BuildContext context) {
    final DateFormat formatter = DateFormat.yMMMMd('en_US');

    return Scaffold(
      appBar: AppBar(
        title: const Text('Plantstagram'),
        centerTitle: true,
      ),
      body: StreamBuilder(
        stream: FirebaseFirestore.instance.collection('posts').snapshots(),
        builder: (BuildContext context, AsyncSnapshot<QuerySnapshot> snapshot) {
          if (snapshot.hasData &&
              // ignore: unnecessary_null_comparison
              snapshot.data!.docs != null &&
              snapshot.data!.docs.isNotEmpty) {
            return Column(
              children: <Widget>[
                ListView.builder(
                    reverse: false,
                    shrinkWrap: true,
                    itemCount: snapshot.data!.docs.length,
                    itemBuilder: (context, index) {
                      var post = snapshot.data!.docs[index];
                      return Semantics(
                        button: true,
                        enabled: true,
                        label: 'a plant entry',
                        onTapHint: 'detailed description of entry',
                        child: ListTile(
                        leading: 
                              Text(
                                formatter.format(post['date'].toDate()),
                                style: const TextStyle(
                                    fontSize: 28, fontWeight: FontWeight.w300),
                                textAlign: TextAlign.right,
                              ),
                        trailing:
                              Text(
                                '${post['itemCount']}',
                                style: const TextStyle(
                                    fontSize: 32, fontWeight: FontWeight.w500),
                                textAlign: TextAlign.left,
                              ),
                        onTap: () {
                          Navigator.pushNamed(context, DetailPost.routeName,
                              arguments: PlantPost(
                                  date: post['date'].toDate(),
                                  photoUrl: post['photoUrl'],
                                  itemCount: post['itemCount'],
                                  latitude: post['latitude'],
                                  longitude: post['longitude'])
                          );
                        },
                        contentPadding: const EdgeInsets.all(10),
                        )
                      );
                    },     
              )
            ]);
          } else {
            return SizedBox(
              height: MediaQuery.of(context).size.height / 1.3,
              child: const Center(child: CircularProgressIndicator()));
              
          }
        },
      ),
      floatingActionButton: Semantics(
        button: true,
        enabled: true,
        onTapHint: 'Select a photo from camera or gallery to make a new entry',
        child: FloatingActionButton(
        child: const Icon(Icons.camera_alt_outlined),
        onPressed: () {
          _showDialog(context);
        },
      )),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }

  Future<void> _showDialog(BuildContext context) async {
    await showDialog(
        context: context,
        builder: (BuildContext context) {
          return Container(
            child: sourceSelection(),
          );
        });
  }

  Widget sourceSelection() {
    return SimpleDialog(
      children: <Widget>[
        Semantics(
          button: true,
          enabled: true,
          onTapHint: 'open the camera option',
          child: SimpleDialogOption(
            padding: const EdgeInsets.all(20),
            child: const Text('Take a photo'),
            onPressed: () async {
              final url = await getImage(ImageSource.camera);
              Navigator.pushReplacementNamed(context, NewPost.routeName,
                  arguments: {'urlLink': url});
            })),
        Semantics(
          button: true,
          enabled: true,
          onTapHint: 'select photo from gallery option',
          child: SimpleDialogOption(
            padding: const EdgeInsets.all(20),
            child: const Text('Choose from Gallery'),
            onPressed: () async {
              final url = await getImage(ImageSource.gallery);
              Navigator.pushReplacementNamed(context, NewPost.routeName,
                  arguments: {'urlLink': url});
            })),
        Semantics(
          button: true,
          enabled: true,
          onTapHint: 'cancel selecting a photo',
          child: SimpleDialogOption(
            padding: const EdgeInsets.all(20),
            child: const Text('Cancel'),
            onPressed: () async {
              Navigator.pop(context);
            })),
      ],
    );
  }
}
