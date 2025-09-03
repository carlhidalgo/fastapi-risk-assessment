import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  TextField,
  MenuItem,
  Button,
  Card,
  CardContent,
  Alert,
  Chip
} from '@mui/material';
import { CompanyService } from '../services/companyService';
import { RiskService } from '../services/riskService';
import { Company } from '../types/company';
import { CreateRiskAssessmentData, RiskAssessmentResponse } from '../types/risk';
import { parseErrorMessage } from '../utils/errorHandler';

const RiskAssessment: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<RiskAssessmentResponse | null>(null);
  const [formData, setFormData] = useState<CreateRiskAssessmentData>({
    company_id: 0,
    requested_amount: 0,
    loan_term_months: 12,
    purpose: '',
    collateral_value: undefined,
    collateral_type: undefined
  });

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      setError(null);
      const companiesData = await CompanyService.getCompanies();
      setCompanies(companiesData);
    } catch (error) {
      console.error('Error loading companies:', error);
      setError(parseErrorMessage(error));
    }
  };

  const handleInputChange = (field: keyof CreateRiskAssessmentData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.value;
    setFormData(prev => ({
      ...prev,
      [field]: field === 'company_id' || field === 'requested_amount' || 
               field === 'loan_term_months' || field === 'collateral_value' 
               ? Number(value) : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const assessment = await RiskService.assessRisk(formData);
      setResult(assessment);
    } catch (error) {
      console.error('Error creating risk assessment:', error);
      setError(parseErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      default: return 'default';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Evaluación de Riesgos
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 3 }}>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            select
            label="Seleccionar Empresa"
            value={formData.company_id || ''}
            onChange={handleInputChange('company_id')}
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
            label="Cantidad Solicitada"
            type="number"
            value={formData.requested_amount}
            onChange={handleInputChange('requested_amount')}
            margin="normal"
            required
            InputProps={{ startAdornment: '$' }}
          />

          <TextField
            fullWidth
            label="Plazo del Préstamo (meses)"
            type="number"
            value={formData.loan_term_months}
            onChange={handleInputChange('loan_term_months')}
            margin="normal"
            required
          />

          <TextField
            fullWidth
            select
            label="Propósito"
            value={formData.purpose}
            onChange={handleInputChange('purpose')}
            margin="normal"
            required
          >
            <MenuItem value="expansion">Expansión del Negocio</MenuItem>
            <MenuItem value="equipment">Compra de Equipos</MenuItem>
            <MenuItem value="working_capital">Capital de Trabajo</MenuItem>
            <MenuItem value="real_estate">Bienes Raíces</MenuItem>
            <MenuItem value="inventory">Inventario</MenuItem>
            <MenuItem value="other">Otros</MenuItem>
          </TextField>

          <TextField
            fullWidth
            label="Valor de Garantía (opcional)"
            type="number"
            value={formData.collateral_value || ''}
            onChange={handleInputChange('collateral_value')}
            margin="normal"
            InputProps={{ startAdornment: '$' }}
          />

          <TextField
            fullWidth
            label="Tipo de Garantía (opcional)"
            value={formData.collateral_type || ''}
            onChange={handleInputChange('collateral_type')}
            margin="normal"
            placeholder="ej. Bienes Raíces, Equipos, Inventario"
          />

          <Box mt={3}>
            <Button
              type="submit"
              variant="contained"
              size="large"
              disabled={loading || !formData.company_id}
              fullWidth
            >
              {loading ? 'Evaluando Riesgo...' : 'Evaluar Riesgo'}
            </Button>
          </Box>
        </form>

        {result && (
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Resultado de Evaluación de Riesgos
              </Typography>
              
              <Box display="flex" alignItems="center" gap={2} mb={2}>
                <Typography variant="h4" component="span">
                  {result.risk_score}/100
                </Typography>
                <Chip 
                  label={result.risk_level}
                  color={getRiskLevelColor(result.risk_level) as any}
                />
              </Box>

              <Alert 
                severity={result.approved ? 'success' : 'error'}
                sx={{ mb: 2 }}
              >
                <Typography variant="body1">
                  <strong>Decisión:</strong> {result.approved ? 'APROBADO' : 'RECHAZADO'}
                </Typography>
                {result.max_approved_amount && (
                  <Typography variant="body2">
                    Cantidad máxima aprobada: {formatCurrency(result.max_approved_amount)}
                  </Typography>
                )}
              </Alert>

              <Typography variant="body1" gutterBottom>
                <strong>Recomendación:</strong> {result.recommendation}
              </Typography>

              <Box mt={2}>
                <Typography variant="body2" color="text.secondary">
                  Evaluación completada para solicitud de préstamo de {formatCurrency(result.requested_amount)} 
                  a {result.loan_term_months} meses para {result.purpose}
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
