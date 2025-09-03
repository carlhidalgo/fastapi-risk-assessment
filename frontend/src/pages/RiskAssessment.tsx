import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  TextField,
  MenuItem,
  Button,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Card,
  CardContent,
  Alert
} from '@mui/material';
import { companiesApi, requestsApi } from '../services/api';

interface Company {
  id: string;
  name: string;
  industry: string;
  size: string;
}

const RiskAssessment: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [formData, setFormData] = useState({
    company_id: '',
    amount: '',
    purpose: '',
    risk_inputs: {
      high_revenue_growth: false,
      stable_market_position: false,
      good_credit_history: false,
      experienced_management: false,
      diversified_revenue: false
    }
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      const response = await companiesApi.getAll();
      setCompanies((response as any).items || []);
    } catch (error) {
      console.error('Error loading companies:', error);
    }
  };

  const calculateRiskScore = (inputs: any) => {
    let score = 50; // Base score
    
    if (inputs.high_revenue_growth) score -= 10;
    if (inputs.stable_market_position) score -= 15;
    if (inputs.good_credit_history) score -= 20;
    if (inputs.experienced_management) score -= 10;
    if (inputs.diversified_revenue) score -= 15;
    
    return Math.max(0, Math.min(100, score));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const riskScore = calculateRiskScore(formData.risk_inputs);
      
      const requestData = {
        company_id: formData.company_id,
        amount: parseFloat(formData.amount),
        purpose: formData.purpose,
        risk_inputs: formData.risk_inputs
      };
      
      const response = await requestsApi.create(requestData);
      setResult({ ...response, risk_score: riskScore });
    } catch (error) {
      console.error('Error creating request:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevel = (score: number) => {
    if (score <= 30) return { level: 'Low Risk', color: 'success' };
    if (score <= 60) return { level: 'Medium Risk', color: 'warning' };
    return { level: 'High Risk', color: 'error' };
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Risk Assessment
      </Typography>

      <Paper sx={{ p: 3 }}>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            select
            label="Select Company"
            value={formData.company_id}
            onChange={(e) => setFormData({ ...formData, company_id: e.target.value })}
            margin="normal"
            required
          >
            {companies.map((company) => (
              <MenuItem key={company.id} value={company.id}>
                {company.name} - {company.industry}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            fullWidth
            label="Loan Amount"
            type="number"
            value={formData.amount}
            onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
            margin="normal"
            required
            InputProps={{ startAdornment: '$' }}
          />

          <TextField
            fullWidth
            select
            label="Purpose"
            value={formData.purpose}
            onChange={(e) => setFormData({ ...formData, purpose: e.target.value })}
            margin="normal"
            required
          >
            <MenuItem value="Expansion">Business Expansion</MenuItem>
            <MenuItem value="Equipment">Equipment Purchase</MenuItem>
            <MenuItem value="Working Capital">Working Capital</MenuItem>
            <MenuItem value="Real Estate">Real Estate</MenuItem>
            <MenuItem value="Other">Other</MenuItem>
          </TextField>

          <Box mt={3}>
            <Typography variant="h6" gutterBottom>
              Risk Factors
            </Typography>
            <FormGroup>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.risk_inputs.high_revenue_growth}
                    onChange={(e) => setFormData({
                      ...formData,
                      risk_inputs: { ...formData.risk_inputs, high_revenue_growth: e.target.checked }
                    })}
                  />
                }
                label="High Revenue Growth (Last 2 years)"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.risk_inputs.stable_market_position}
                    onChange={(e) => setFormData({
                      ...formData,
                      risk_inputs: { ...formData.risk_inputs, stable_market_position: e.target.checked }
                    })}
                  />
                }
                label="Stable Market Position"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.risk_inputs.good_credit_history}
                    onChange={(e) => setFormData({
                      ...formData,
                      risk_inputs: { ...formData.risk_inputs, good_credit_history: e.target.checked }
                    })}
                  />
                }
                label="Good Credit History"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.risk_inputs.experienced_management}
                    onChange={(e) => setFormData({
                      ...formData,
                      risk_inputs: { ...formData.risk_inputs, experienced_management: e.target.checked }
                    })}
                  />
                }
                label="Experienced Management Team"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.risk_inputs.diversified_revenue}
                    onChange={(e) => setFormData({
                      ...formData,
                      risk_inputs: { ...formData.risk_inputs, diversified_revenue: e.target.checked }
                    })}
                  />
                }
                label="Diversified Revenue Streams"
              />
            </FormGroup>
          </Box>

          <Box mt={3}>
            <Button
              type="submit"
              variant="contained"
              size="large"
              disabled={loading}
              fullWidth
            >
              {loading ? 'Calculating...' : 'Calculate Risk Score'}
            </Button>
          </Box>
        </form>

        {result && (
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Risk Assessment Result
              </Typography>
              <Alert severity={getRiskLevel(result.risk_score).color as any}>
                <Typography variant="h4" component="span">
                  {result.risk_score}/100
                </Typography>
                <Typography variant="body1" component="span" sx={{ ml: 2 }}>
                  {getRiskLevel(result.risk_score).level}
                </Typography>
              </Alert>
              <Box mt={2}>
                <Typography variant="body2" color="text.secondary">
                  Assessment completed for ${parseFloat(formData.amount).toLocaleString()} loan request
                </Typography>
              </Box>
            </CardContent>
          </Card>
        )}
      </Paper>
    </Container>
  );
};

export default RiskAssessment;
