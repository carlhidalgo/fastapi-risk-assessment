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
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import { CompanyService } from '../services/companyService';
import { RequestService } from '../services/requestService';
import { Company } from '../types/company';
import { RiskRequest } from '../types/request';
import { ROUTES } from '../constants/config';
import { FadeInUp, StaggerContainer, ListItem } from '../components/PageTransition';
import { EnhancedCard, StatusChip } from '../components/EnhancedComponents';
import { LoadingSpinner } from '../components/LoadingComponents';

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

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <LoadingSpinner message="Cargando dashboard..." />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <FadeInUp>
        <Box mb={4}>
          <Typography variant="h3" component="h1" gutterBottom className="text-gradient">
            Bienvenido de nuevo, {user?.full_name || 'Usuario'}!
          </Typography>
          <Typography variant="h6" color="text.secondary">
            Panel de la Plataforma de Evaluación de Riesgos
          </Typography>
        </Box>
      </FadeInUp>

      <StaggerContainer delay={0.1}>
        <Box display="flex" gap={3} mb={4} flexWrap="wrap">
          <ListItem>
            <Box flex="1" minWidth={250}>
              <EnhancedCard delay={0}>
                <Box display="flex" alignItems="center" mb={2}>
                  <motion.div
                    animate={{ rotate: [0, 10, -10, 0] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                  >
                    <Business color="primary" sx={{ mr: 1 }} />
                  </motion.div>
                  <Typography variant="h6">Empresas</Typography>
                </Box>
                <Typography variant="h3" color="primary">
                  {stats.totalCompanies}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total de empresas registradas
                </Typography>
              </EnhancedCard>
            </Box>
          </ListItem>

          <ListItem>
            <Box flex="1" minWidth={250}>
              <EnhancedCard delay={0.1}>
                <Box display="flex" alignItems="center" mb={2}>
                  <motion.div
                    animate={{ scale: [1, 1.1, 1] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                  >
                    <Assessment color="secondary" sx={{ mr: 1 }} />
                  </motion.div>
                  <Typography variant="h6">Industrias</Typography>
                </Box>
                <Typography variant="h3" color="secondary">
                  {stats.industries}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Diferentes industrias cubiertas
                </Typography>
              </EnhancedCard>
            </Box>
          </ListItem>

          <ListItem>
            <Box flex="1" minWidth={250}>
              <EnhancedCard delay={0.2}>
                <Box display="flex" alignItems="center" mb={2}>
                  <motion.div
                    animate={{ y: [0, -5, 0] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                  >
                    <TrendingUp color="info" sx={{ mr: 1 }} />
                  </motion.div>
                  <Typography variant="h6">Evaluaciones</Typography>
                </Box>
                <Typography variant="h3" color="info.main">
                  {stats.totalRequests}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Evaluaciones de riesgo realizadas
                </Typography>
              </EnhancedCard>
            </Box>
          </ListItem>
        </Box>
      </StaggerContainer>

      <StaggerContainer delay={0.2}>
        <Box display="flex" gap={3} flexWrap="wrap">
          <ListItem>
            <Box flex="1" minWidth={400}>
              <EnhancedCard delay={0}>
                <Typography variant="h5" gutterBottom>
                  Acciones Rápidas
                </Typography>
                <Box display="flex" flexDirection="column" gap={2}>
                  <motion.div
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <Button
                      variant="contained"
                      size="large"
                      startIcon={<Add />}
                      component={Link}
                      to={ROUTES.COMPANIES}
                      fullWidth
                      className="hover-glow"
                    >
                      Agregar Nueva Empresa
                    </Button>
                  </motion.div>
                  <motion.div
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <Button
                      variant="outlined"
                      size="large"
                      startIcon={<Assessment />}
                      component={Link}
                      to={ROUTES.RISK_ASSESSMENT}
                      fullWidth
                      className="hover-lift"
                    >
                      Evaluar Riesgo
                    </Button>
                  </motion.div>
                </Box>
              </EnhancedCard>
            </Box>
          </ListItem>

          <ListItem>
            <Box flex="1" minWidth={400}>
              <EnhancedCard delay={0.1}>
                <Typography variant="h5" gutterBottom>
                  Evaluaciones de Riesgo Recientes
                </Typography>
                {recentRequests.length > 0 ? (
                  <StaggerContainer delay={0.1}>
                    {recentRequests.slice(0, 3).map((request, index) => {
                      const company = companies.find(c => c.id.toString() === request.company_id);
                      return (
                        <ListItem key={request.id}>
                          <motion.div
                            className="hover-lift"
                            style={{ width: '100%' }}
                          >
                            <Box 
                              mb={2} 
                              p={2} 
                              border="1px solid #e0e0e0" 
                              borderRadius={2}
                              sx={{ 
                                background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
                                transition: 'all 0.2s ease'
                              }}
                            >
                              <Box display="flex" justifyContent="space-between" alignItems="start" mb={1}>
                                <Typography variant="subtitle1" fontWeight="bold">
                                  {company?.name || 'Empresa Desconocida'}
                                </Typography>
                                <StatusChip
                                  label={request.risk_level}
                                  color={getRiskLevelColor(request.risk_level) as any}
                                  delay={index * 0.1}
                                />
                              </Box>
                              <Typography variant="body2" color="text.secondary">
                                Monto: ${request.amount.toLocaleString()} USD
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
                          </motion.div>
                        </ListItem>
                      );
                    })}
                  </StaggerContainer>
                ) : (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 }}
                  >
                    <Typography color="text.secondary">
                      No hay evaluaciones de riesgo registradas aún.
                    </Typography>
                  </motion.div>
                )}
              </EnhancedCard>
            </Box>
          </ListItem>
        </Box>
      </StaggerContainer>
    </Container>
  );
};

export default Dashboard;
