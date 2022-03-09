import 'package:flutter/material.dart';
import 'package:flutter_application_5/screens/new_plant_screen.dart';
import 'package:flutter_application_5/screens/plant_detail_screen.dart';
import 'screens/plant_list_screen.dart';
import 'package:firebase_core/firebase_core.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(const App(title: 'Plantstagram'));
}

class App extends StatelessWidget {
  final String title;

  const App({Key? key, required this.title}) : super(key: key);

  static final routes = {
    NewPost.routeName: (context) => const NewPost(),
    CameraScreen.routeName: (context) => const CameraScreen(),
    DetailPost.routeName: (context) => const DetailPost()
  };

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'Plantstagram',
        theme: ThemeData.dark(),
        // class from plant_list_screen.dart
        home: const CameraScreen(),
        routes: routes);
  }
}
