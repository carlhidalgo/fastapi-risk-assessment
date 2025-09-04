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
    company_id: '',
    amount: 0,
    purpose: '',
    annual_revenue: undefined,
    employee_count: undefined,
    years_in_business: undefined,
    debt_to_equity_ratio: undefined,
    credit_score: undefined
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
      [field]: field === 'company_id' || field === 'purpose' 
               ? value 
               : field === 'amount' || field === 'annual_revenue' || 
                 field === 'employee_count' || field === 'years_in_business' ||
                 field === 'debt_to_equity_ratio' || field === 'credit_score'
               ? Number(value) || undefined 
               : value
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
              <MenuItem key={company.id} value={company.id.toString()}>
                {company.name} - {company.industry}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            fullWidth
            label="Cantidad Solicitada"
            type="number"
            value={formData.amount || ''}
            onChange={handleInputChange('amount')}
            margin="normal"
            required
            InputProps={{ startAdornment: '$' }}
          />

          <TextField
            fullWidth
            label="Propósito del Préstamo"
            value={formData.purpose}
            onChange={handleInputChange('purpose')}
            margin="normal"
            required
            placeholder="Ej: Expansión del negocio, capital de trabajo, equipamiento"
          />

          <TextField
            fullWidth
            label="Ingresos Anuales (Opcional)"
            type="number"
            value={formData.annual_revenue || ''}
            onChange={handleInputChange('annual_revenue')}
            margin="normal"
            InputProps={{ startAdornment: '$' }}
          />

          <TextField
            fullWidth
            label="Número de Empleados (Opcional)"
            type="number"
            value={formData.employee_count || ''}
            onChange={handleInputChange('employee_count')}
            margin="normal"
          />

          <TextField
            fullWidth
            label="Años en el Negocio (Opcional)"
            type="number"
            value={formData.years_in_business || ''}
            onChange={handleInputChange('years_in_business')}
            margin="normal"
          />

          <TextField
            fullWidth
            label="Ratio Deuda/Patrimonio (Opcional)"
            type="number"
            value={formData.debt_to_equity_ratio || ''}
            onChange={handleInputChange('debt_to_equity_ratio')}
            margin="normal"
            inputProps={{ step: "0.01", min: "0" }}
          />

          <TextField
            fullWidth
            label="Puntuación Crediticia (Opcional)"
            type="number"
            value={formData.credit_score || ''}
            onChange={handleInputChange('credit_score')}
            margin="normal"
            inputProps={{ min: "300", max: "850" }}
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
              </Alert>

              <Typography variant="h6" gutterBottom>
                Recomendaciones:
              </Typography>
              {result.recommendations && result.recommendations.length > 0 ? (
                <Box component="ul" sx={{ mt: 1, pl: 2 }}>
                  {result.recommendations.map((recommendation, index) => (
                    <Typography key={index} component="li" variant="body2" gutterBottom>
                      {recommendation}
                    </Typography>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No hay recomendaciones específicas disponibles.
                </Typography>
              )}

              <Box mt={2}>
                <Typography variant="body2" color="text.secondary">
                  Evaluación completada para solicitud de préstamo de ${formData.amount?.toLocaleString()} 
                  para {formData.purpose}
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
