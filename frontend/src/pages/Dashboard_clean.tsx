import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Card,
  CardContent,
  Button
} from '@mui/material';
import { Link } from 'react-router-dom';
import { Add, Business, Assessment } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { CompanyService } from '../services/companyService';
import { Company } from '../types/company';
import { ROUTES } from '../constants/config';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      const companiesData = await CompanyService.getCompanies();
      setCompanies(companiesData);
    } catch (error) {
      console.error('Error loading companies:', error);
    } finally {
      setLoading(false);
    }
  };

  const stats = {
    totalCompanies: companies.length,
    averageRevenue: companies.length > 0 
      ? companies.reduce((sum, c) => sum + c.annual_revenue, 0) / companies.length 
      : 0,
    industries: Array.from(new Set(companies.map(c => c.industry))).length
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box mb={4}>
        <Typography variant="h3" component="h1" gutterBottom>
          Bienvenido de nuevo, {user?.name}!
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
                <Assessment color="success" sx={{ mr: 1 }} />
                <Typography variant="h6">Ingresos Promedio</Typography>
              </Box>
              <Typography variant="h3" color="success.main">
                ${Math.round(stats.averageRevenue / 1000)}K
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Ingresos anuales promedio
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
              Empresas Recientes
            </Typography>
            {loading ? (
              <Typography>Cargando...</Typography>
            ) : companies.length > 0 ? (
              <Box>
                {companies.slice(-3).reverse().map((company) => (
                  <Box key={company.id} mb={2} p={2} border="1px solid #e0e0e0" borderRadius={1}>
                    <Typography variant="subtitle1" fontWeight="bold">
                      {company.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {company.industry} • {company.company_size} empleados
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Ingresos: ${company.annual_revenue.toLocaleString()}
                    </Typography>
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography color="text.secondary">
                No hay empresas registradas aún. <Link to={ROUTES.COMPANIES}>Agrega tu primera empresa</Link>
              </Typography>
            )}
          </Paper>
        </Box>
      </Box>
    </Container>
  );
};

export default Dashboard;
