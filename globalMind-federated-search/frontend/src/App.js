import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Grid,
  Box,
  Chip,
  CircularProgress,
  Alert,
  Paper,
  AppBar,
  Toolbar,
  IconButton,
  Fade,
  Divider
} from '@mui/material';
import {
  Search as SearchIcon,
  Language as LanguageIcon,
  Timer as TimerIcon,
  TrendingUp as TrendingUpIcon,
  Psychology as PsychologyIcon
} from '@mui/icons-material';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [query, setQuery] = useState('');
  const [language, setLanguage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState('');
  const [exampleQueries, setExampleQueries] = useState({});
  const [languageInfo, setLanguageInfo] = useState({});

  useEffect(() => {
    // Load example queries and language info on component mount
    loadExampleQueries();
    loadLanguageInfo();
  }, []);

  const loadExampleQueries = async () => {
    try {
      const result = await axios.get(`${API_BASE_URL}/api/v1/examples`);
      setExampleQueries(result.data.example_queries);
    } catch (err) {
      console.error('Failed to load example queries:', err);
    }
  };

  const loadLanguageInfo = async () => {
    try {
      const result = await axios.get(`${API_BASE_URL}/api/v1/languages`);
      setLanguageInfo(result.data.supported_languages);
    } catch (err) {
      console.error('Failed to load language info:', err);
    }
  };

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('कृपया प्रश्न दर्ज करें / Please enter a query');
      return;
    }

    setIsLoading(true);
    setError('');
    setResponse(null);

    try {
      const result = await axios.post(`${API_BASE_URL}/api/v1/query`, {
        query: query,
        language: language || null
      });

      setResponse(result.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'कुछ गलत हुआ है / Something went wrong');
    } finally {
      setIsLoading(false);
    }
  };

  const handleExampleQuery = (exampleQuery) => {
    setQuery(exampleQuery);
    setError('');
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  const formatResponseContent = (responseData) => {
    if (!responseData.response) return null;

    const { response: resp } = responseData;

    return (
      <Card elevation={3} sx={{ mt: 2 }}>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <PsychologyIcon sx={{ mr: 1, color: 'primary.main' }} />
            <Typography variant="h6" color="primary">
              AI Response - {getLanguageName(responseData.detected_language)}
            </Typography>
          </Box>

          {/* Query Information */}
          <Box mb={2}>
            <Typography variant="body2" color="text.secondary">
              <strong>Query:</strong> {responseData.query}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              <strong>Detected Language:</strong> {responseData.detected_language}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              <strong>Processing Time:</strong> {responseData.processing_time_ms}ms
            </Typography>
          </Box>

          <Divider sx={{ my: 2 }} />

          {/* Cultural Context */}
          {resp.cultural_context && (
            <Box mb={2}>
              <Typography variant="subtitle1" color="primary" gutterBottom>
                🎭 Cultural Context Detected:
              </Typography>
              {resp.cultural_context.festivals?.length > 0 && (
                <Box mb={1}>
                  <Typography variant="body2"><strong>Festivals:</strong></Typography>
                  {resp.cultural_context.festivals.map((festival, index) => (
                    <Chip
                      key={index}
                      label={`${festival.name} (${festival.english})`}
                      size="small"
                      sx={{ mr: 1, mb: 1 }}
                      color="secondary"
                    />
                  ))}
                </Box>
              )}
              {resp.cultural_context.food_items?.length > 0 && (
                <Box mb={1}>
                  <Typography variant="body2"><strong>Food Items:</strong></Typography>
                  {resp.cultural_context.food_items.map((food, index) => (
                    <Chip
                      key={index}
                      label={food.item}
                      size="small"
                      sx={{ mr: 1, mb: 1 }}
                      color="success"
                    />
                  ))}
                </Box>
              )}
            </Box>
          )}

          {/* Response Content */}
          <Box>
            <Typography variant="subtitle1" color="primary" gutterBottom>
              📋 Response:
            </Typography>
            
            {resp.response?.type === 'cultural_guide' && (
              <Box>
                <Typography variant="h6" gutterBottom>{resp.response.title}</Typography>
                <Typography variant="body1" sx={{ whiteSpace: 'pre-line', mb: 2 }}>
                  {resp.response.content}
                </Typography>
                {resp.response.traditional_practices && (
                  <Box>
                    <Typography variant="subtitle2" gutterBottom>Traditional Practices:</Typography>
                    <ul>
                      {resp.response.traditional_practices.map((practice, index) => (
                        <li key={index}>{practice}</li>
                      ))}
                    </ul>
                  </Box>
                )}
              </Box>
            )}

            {resp.response?.type === 'healthcare_advice' && (
              <Box>
                <Typography variant="body1" gutterBottom>
                  <strong>Condition:</strong> {resp.response.condition}
                </Typography>
                <Typography variant="subtitle2" gutterBottom>Traditional Remedies:</Typography>
                <ul>
                  {resp.response.traditional_remedies.map((remedy, index) => (
                    <li key={index}>{remedy}</li>
                  ))}
                </ul>
                <Alert severity="info" sx={{ mt: 2 }}>
                  {resp.response.disclaimer}
                </Alert>
              </Box>
            )}

            {resp.response?.type === 'general_response' && (
              <Typography variant="body1">{resp.response.content}</Typography>
            )}
          </Box>

          {/* Performance Metrics */}
          <Box mt={2} p={2} bgcolor="grey.50" borderRadius={1}>
            <Typography variant="caption" color="text.secondary">
              Intent: {resp.intent} | Confidence: {resp.confidence} | Script: {resp.script?.primary_script}
            </Typography>
          </Box>
        </CardContent>
      </Card>
    );
  };

  const getLanguageName = (code) => {
    const names = {
      'hindi': 'हिंदी (Hindi)',
      'telugu': 'తెలుగు (Telugu)',
      'marathi': 'मराठी (Marathi)'
    };
    return names[code] || code;
  };

  return (
    <div className="App">
      {/* Header */}
      <AppBar position="static" sx={{ bgcolor: 'primary.main' }}>
        <Toolbar>
          <PsychologyIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            GlobalMind FL - Multilingual AI Search
          </Typography>
          <Box display="flex" alignItems="center">
            <LanguageIcon sx={{ mr: 1 }} />
            <Typography variant="body2">हिंदी | తెలుగు | मराठी</Typography>
          </Box>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        {/* Hero Section */}
        <Box textAlign="center" mb={4}>
          <Typography variant="h3" component="h1" gutterBottom color="primary">
            🌍 GlobalMind FL
          </Typography>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Federated Learning for Multilingual AI Search Intelligence
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Privacy-preserving, culturally-aware AI search for Hindi, Telugu & Marathi speakers
          </Typography>
        </Box>

        {/* Search Interface */}
        <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={8}>
              <TextField
                fullWidth
                variant="outlined"
                placeholder="अपना प्रश्न यहाँ लिखें / మీ ప్రశ్న ఇక్కడ రాయండి / तुमचा प्रश्न इथे लिहा"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isLoading}
                InputProps={{
                  style: { fontSize: '16px' }
                }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <Button
                fullWidth
                variant="contained"
                size="large"
                onClick={handleSearch}
                disabled={isLoading || !query.trim()}
                startIcon={isLoading ? <CircularProgress size={20} /> : <SearchIcon />}
                sx={{ height: '56px' }}
              >
                {isLoading ? 'Processing...' : 'Search'}
              </Button>
            </Grid>
          </Grid>

          {/* Language Selection */}
          <Box mt={2}>
            <Typography variant="body2" gutterBottom>
              Language (Optional - Auto-detected if not specified):
            </Typography>
            <Box>
              {['', 'hindi', 'telugu', 'marathi'].map((lang) => (
                <Button
                  key={lang}
                  variant={language === lang ? 'contained' : 'outlined'}
                  size="small"
                  onClick={() => setLanguage(lang)}
                  sx={{ mr: 1, mb: 1 }}
                >
                  {lang === '' ? 'Auto-detect' : getLanguageName(lang)}
                </Button>
              ))}
            </Box>
          </Box>
        </Paper>

        {/* Error Display */}
        {error && (
          <Fade in={!!error}>
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          </Fade>
        )}

        {/* Response Display */}
        {response && (
          <Fade in={!!response}>
            <div>{formatResponseContent(response)}</div>
          </Fade>
        )}

        {/* Example Queries */}
        {Object.keys(exampleQueries).length > 0 && !response && (
          <Paper elevation={2} sx={{ p: 3, mt: 4 }}>
            <Typography variant="h6" gutterBottom color="primary">
              🔍 Example Queries
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Click on any example to try it:
            </Typography>
            
            {Object.entries(exampleQueries).map(([lang, queries]) => (
              <Box key={lang} mb={3}>
                <Typography variant="subtitle1" gutterBottom>
                  {getLanguageName(lang)}:
                </Typography>
                <Grid container spacing={1}>
                  {queries.map((example, index) => (
                    <Grid item xs={12} sm={6} md={6} key={index}>
                      <Button
                        variant="outlined"
                        size="small"
                        onClick={() => handleExampleQuery(example)}
                        sx={{ 
                          textAlign: 'left',
                          justifyContent: 'flex-start',
                          width: '100%',
                          textTransform: 'none',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap'
                        }}
                      >
                        {example}
                      </Button>
                    </Grid>
                  ))}
                </Grid>
              </Box>
            ))}
          </Paper>
        )}

        {/* Language Information */}
        {Object.keys(languageInfo).length > 0 && !response && (
          <Paper elevation={2} sx={{ p: 3, mt: 4 }}>
            <Typography variant="h6" gutterBottom color="primary">
              🗣️ Supported Languages
            </Typography>
            <Grid container spacing={3}>
              {Object.entries(languageInfo).map(([key, info]) => (
                <Grid item xs={12} md={4} key={key}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        {info.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        <strong>Script:</strong> {info.script}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        <strong>Speakers:</strong> {info.speakers}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        <strong>Regions:</strong> {info.regions.join(', ')}
                      </Typography>
                      <Box mt={1}>
                        {info.cultural_domains.map((domain, index) => (
                          <Chip
                            key={index}
                            label={domain}
                            size="small"
                            sx={{ mr: 0.5, mb: 0.5 }}
                            variant="outlined"
                          />
                        ))}
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        )}

        {/* Footer */}
        <Box mt={6} textAlign="center" color="text.secondary">
          <Typography variant="body2">
            Built with ❤️ for 800+ Million Indian Language Speakers
          </Typography>
          <Typography variant="caption">
            Privacy-preserving • Culturally-aware • Federated Learning
          </Typography>
        </Box>
      </Container>
    </div>
  );
}

export default App;
