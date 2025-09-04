import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Card,
  CardContent,
  Button,
  Chip
} from '@mui/material';
import { Link } from 'react-router-dom';
import { Add, Business, Assessment, TrendingUp } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { CompanyService } from '../services/companyService';
import { RequestService } from '../services/requestService';
import { Company } from '../types/company';
import { RiskRequest } from '../types/request';
import { ROUTES } from '../constants/config';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [recentRequests, setRecentRequests] = useState<RiskRequest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [companiesData, requestsData] = await Promise.all([
        CompanyService.getCompanies(),
        RequestService.getRequests({ page: 1, size: 5 })
      ]);
      setCompanies(companiesData);
      setRecentRequests(requestsData.items);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const stats = {
    totalCompanies: companies.length,
    totalRequests: recentRequests.length,
    averageRevenue: companies.length > 0 
      ? companies.reduce((sum, c) => sum + c.annual_revenue, 0) / companies.length 
      : 0,
    industries: Array.from(new Set(companies.map(c => c.industry))).length,
    approvedRequests: recentRequests.filter(r => r.approved).length
  };

  const getRiskLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'bajo':
      case 'low':
        return 'success';
      case 'medio':
      case 'medium':
        return 'warning';
      case 'alto':
      case 'high':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box mb={4}>
        <Typography variant="h3" component="h1" gutterBottom>
          Bienvenido de nuevo, {user?.full_name || 'Usuario'}!
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Panel de la Plataforma de Evaluación de Riesgos
        </Typography>
      </Box>

      <Box display="flex" gap={3} mb={4} flexWrap="wrap">
        <Box flex="1" minWidth={250}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Business color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Empresas</Typography>
              </Box>
              <Typography variant="h3" color="primary">
                {stats.totalCompanies}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total de empresas registradas
              </Typography>
            </CardContent>
          </Card>
        </Box>

        <Box flex="1" minWidth={250}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Assessment color="secondary" sx={{ mr: 1 }} />
                <Typography variant="h6">Industrias</Typography>
              </Box>
              <Typography variant="h3" color="secondary">
                {stats.industries}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Diferentes industrias cubiertas
              </Typography>
            </CardContent>
          </Card>
        </Box>

        <Box flex="1" minWidth={250}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <TrendingUp color="info" sx={{ mr: 1 }} />
                <Typography variant="h6">Evaluaciones</Typography>
              </Box>
              <Typography variant="h3" color="info.main">
                {stats.totalRequests}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Evaluaciones de riesgo realizadas
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>

      <Box display="flex" gap={3} flexWrap="wrap">
        <Box flex="1" minWidth={400}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Acciones Rápidas
            </Typography>
            <Box display="flex" flexDirection="column" gap={2}>
              <Button
                variant="contained"
                size="large"
                startIcon={<Add />}
                component={Link}
                to={ROUTES.COMPANIES}
                fullWidth
              >
                Agregar Nueva Empresa
              </Button>
              <Button
                variant="outlined"
                size="large"
                startIcon={<Assessment />}
                component={Link}
                to={ROUTES.RISK_ASSESSMENT}
                fullWidth
              >
                Evaluar Riesgo
              </Button>
            </Box>
          </Paper>
        </Box>

        <Box flex="1" minWidth={400}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Evaluaciones de Riesgo Recientes
            </Typography>
            {loading ? (
              <Typography>Cargando...</Typography>
            ) : recentRequests.length > 0 ? (
              <Box>
                {recentRequests.slice(0, 3).map((request) => {
                  const company = companies.find(c => c.id.toString() === request.company_id);
                  return (
                    <Box key={request.id} mb={2} p={2} border="1px solid #e0e0e0" borderRadius={1}>
                      <Box display="flex" justifyContent="space-between" alignItems="start" mb={1}>
                        <Typography variant="subtitle1" fontWeight="bold">
                          {company?.name || 'Empresa Desconocida'}
                        </Typography>
                        <Chip
                          label={request.risk_level}
                          color={getRiskLevelColor(request.risk_level) as any}
                          size="small"
                        />
                      </Box>
                      <Typography variant="body2" color="text.secondary">
                        Monto: ${request.amount.toLocaleString()}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Puntuación: {request.risk_score}/100
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Estado: {request.approved ? 'Aprobado' : 'Rechazado'}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {new Date(request.created_at).toLocaleDateString('es-ES')}
                      </Typography>
                    </Box>
                  );
                })}
              </Box>
            ) : (
              <Typography color="text.secondary">
                No hay evaluaciones de riesgo registradas aún.
              </Typography>
            )}
          </Paper>
        </Box>
      </Box>
    </Container>
  );
};

export default Dashboard;
