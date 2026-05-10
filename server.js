import express from 'express';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the current directory
app.use(express.static(__dirname));

// Frontend Routes
app.get('/', (req, res) => {
  res.sendFile(join(__dirname, 'landing.html'));
});

app.get('/login', (req, res) => {
  res.sendFile(join(__dirname, 'login.html'));
});

app.get('/signup', (req, res) => {
  res.sendFile(join(__dirname, 'signup.html'));
});

app.get('/docs', (req, res) => {
  res.sendFile(join(__dirname, 'docs.html'));
});

app.get('/components', (req, res) => {
  res.sendFile(join(__dirname, 'components.html'));
});

// API routes for authentication (to be implemented with your backend)
app.post('/api/login', (req, res) => {
  const { email, password } = req.body;
  
  // TODO: Implement actual authentication with your database
  // Example validation
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password required' });
  }

  // Placeholder response
  res.json({ 
    success: true, 
    message: 'Login successful',
    user: { email, id: 'user_id' },
    token: 'jwt_token_here'
  });
});

app.post('/api/signup', (req, res) => {
  const { fullname, email, password, confirmpassword } = req.body;
  
  // TODO: Implement actual registration with your database
  // Validation
  if (!fullname || !email || !password || !confirmpassword) {
    return res.status(400).json({ error: 'All fields required' });
  }

  if (password !== confirmpassword) {
    return res.status(400).json({ error: 'Passwords do not match' });
  }

  if (password.length < 8) {
    return res.status(400).json({ error: 'Password must be at least 8 characters' });
  }

  // Placeholder response
  res.json({ 
    success: true, 
    message: 'Account created successfully',
    user: { email, fullname, id: 'user_id' }
  });
});

app.listen(PORT, () => {
  console.log(`\n🎬 CinAImatic Server Running`);
  console.log(`📍 http://localhost:${PORT}`);
  console.log(`📖 Documentation: http://localhost:${PORT}/docs`);
  console.log(`🎨 Components: http://localhost:${PORT}/components`);
  console.log(`🌐 Open the landing page in your browser\n`);
});
