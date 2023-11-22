import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:image_picker/image_picker.dart';
import 'dart:io'; // Import Dart IO to use File

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Campus Safety Reporting System',
      theme: ThemeData(
        primarySwatch: Colors.purple,
      ),
      home: LoginScreen(),
    );
  }
}

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  Future<void> _login() async {
    final response = await http.post(
      Uri.parse('http://localhost:3000/api/login'),
      headers: <String, String>{
        'Content-Type': 'application/json',
      },
      body: jsonEncode(<String, String>{
        'username': _usernameController.text,
        'password': _passwordController.text,
      }),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data['role'] != null) {
        _navigateToDashboard(data['role'], _usernameController.text);
        // Passing username to dashboard
      } else {
        // Show error message
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Invalid username or password')),
        );
      }
    } else {
      // Handle server error
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Server error: ${response.statusCode}')),
      );
    }
  }

  void _navigateToDashboard(String role, String username) {
    if (role == 'moderator') {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => ModeratorDashboard()),
      );
    }
    if (role == 'user') {
      Navigator.push(
        context,
        MaterialPageRoute(
            builder: (context) => UserDashboard(username: username)),
      );
    } else {
      // Navigate to other dashboards based on role
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Login to Campus Safety System")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            TextField(
              controller: _usernameController,
              decoration: InputDecoration(labelText: 'Username'),
            ),
            SizedBox(height: 8.0),
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: InputDecoration(labelText: 'Password'),
            ),
            SizedBox(height: 20.0),
            ElevatedButton(
              onPressed: _login,
              child: Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
}

// Add your dashboard screens here

class ModeratorDashboard extends StatefulWidget {
  @override
  _ModeratorDashboardState createState() => _ModeratorDashboardState();
}

class _ModeratorDashboardState extends State<ModeratorDashboard> {
  List<dynamic> reports = [];

  @override
  void initState() {
    super.initState();
    _fetchReports();
  }

  Future<void> _fetchReports() async {
    try {
      final response =
          await http.get(Uri.parse('http://localhost:3000/api/reports'));
      if (response.statusCode == 200) {
        setState(() {
          reports = json.decode(response.body);
        });
      } else {
        // Handle server error
      }
    } catch (e) {
      // Handle network error
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Moderator Dashboard"),
        // AppBar code
      ),
      body: ListView.builder(
        itemCount: reports.length,
        itemBuilder: (context, index) {
          final report = reports[index];
          return Card(
            child: ListTile(
              title: Text(report['username']),
              subtitle: Text(
                  "${report['timestamp']} - ${report['emergency_level']} - ${report['location']} - ${report['report']}"),
              // rest of your code...
            ),
          );
        },
      ),
    );
  }
}

class UserDashboard extends StatefulWidget {
  final String username;

  UserDashboard({required this.username});

  @override
  _UserDashboardState createState() => _UserDashboardState();
}

class _UserDashboardState extends State<UserDashboard> {
  final TextEditingController _reportController = TextEditingController();
  final ImagePicker _picker = ImagePicker();
  XFile? _image; // State variable to store the picked image

  void _pickImage() async {
    final XFile? pickedImage =
        await _picker.pickImage(source: ImageSource.gallery);
    if (pickedImage != null) {
      setState(() {
        _image = pickedImage;
      });
    }
    // Handle the case when the user doesn't pick an image
  }

  void _submitReport(BuildContext context) {
    // Logic to handle the submission of the report
    // This should include sending the report and the screenshot to the server
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("User Dashboard"),
        actions: <Widget>[
          IconButton(
            icon: Icon(Icons.settings),
            onPressed: () {
              // Navigate to settings
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Text(
                'Welcome, ${widget.username}',
                style: TextStyle(fontSize: 24),
              ),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                shape: CircleBorder(),
                padding: EdgeInsets.all(24),
                primary: Colors.red,
              ),
              child: Icon(Icons.warning, size: 48),
              onPressed: () {
                // Panic button functionality
              },
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: TextField(
                controller: _reportController,
                decoration: InputDecoration(
                  labelText: 'Describe the sexist activity',
                  border: OutlineInputBorder(),
                ),
                maxLines: 3,
              ),
            ),
            ElevatedButton(
              onPressed: _pickImage,
              child: Text('Upload Screenshot'),
            ),
            // Display the selected image
            if (_image != null) Image.file(File(_image!.path)),
            ElevatedButton(
              onPressed: () => _submitReport(context),
              child: Text('Submit Report'),
            ),
          ],
        ),
      ),
    );
  }
}
// Similarly, add UserDashboard and EmployeeDashboard
