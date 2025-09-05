import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  TextField,
  Box,
  Alert,
  CircularProgress,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Fab
} from '@mui/material';
import { Add, Edit, Delete, ArrowBack, TrendingUp, Assessment } from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { CompanyService } from '../services/companyService';
import { RequestService } from '../services/requestService';
import { Company } from '../types/company';
import { RiskRequest, RequestFormData } from '../types/request';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

const RiskAssessment: React.FC = () => {
  const { companyId } = useParams<{ companyId: string }>();
  const navigate = useNavigate();

  // Estado principal
  const [company, setCompany] = useState<Company | null>(null);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [requests, setRequests] = useState<RiskRequest[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Estado del formulario
  const [open, setOpen] = useState(false);
  const [editingRequest, setEditingRequest] = useState<RiskRequest | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [requestToDelete, setRequestToDelete] = useState<RiskRequest | null>(null);

  const [formData, setFormData] = useState<RequestFormData>({
    company_id: companyId || '',
    amount: 0,
    purpose: '',
    credit_score: 0,
    debt_to_equity_ratio: 0,
    years_in_business: 0,
    cash_flow: 0
  });

  // Cargar datos de la empresa
  const loadCompany = async () => {
    if (!companyId) return;
    
    try {
      const companyData = await CompanyService.getCompany(parseInt(companyId));
      setCompany(companyData);
    } catch (error) {
      console.error('Error loading company:', error);
      setError('Error al cargar la empresa');
    }
  };

  // Cargar todas las empresas (necesario para ambas vistas)
  const loadCompanies = async () => {
    try {
      console.log('Loading companies...');
      const companiesData = await CompanyService.getCompanies();
      console.log('Companies loaded successfully:', companiesData);
      setCompanies(companiesData);
    } catch (error) {
      console.error('Error loading companies:', error);
    }
  };

  // Cargar evaluaciones de riesgo
  const loadRequests = async () => {
    try {
      // Si hay companyId, filtrar por empresa específica, si no, mostrar todas
      const params = companyId ? { company_id: companyId } : {};
      const requestsData = await RequestService.getRequests(params);
      setRequests(requestsData.items);
    } catch (error) {
      console.error('Error loading requests:', error);
      setError('Error al cargar las evaluaciones de riesgo');
    }
  };

  useEffect(() => {
    const loadData = async () => {
      console.log('useEffect triggered, companyId:', companyId);
      
      // Limpiar estado anterior cuando se cambia de vista
      setError(null);
      setLoading(true);
      
      // Limpiar estado específico basado en el tipo de vista
      if (companyId) {
        // Vista específica de empresa: limpiar companies array y cargar empresa específica
        console.log('Loading specific company view');
        setCompanies([]);
        await loadCompany();
      } else {
        // Vista general: limpiar company específica
        console.log('Loading general view');
        setCompany(null);
      }
      
      // Siempre cargar empresas (necesario para resolver nombres) y requests
      await loadCompanies();
      await loadRequests();
      
      setLoading(false);
    };
    loadData();
  }, [companyId]);

  const parseErrorMessage = (error: any): string => {
    if (error?.response?.data?.detail) {
      if (Array.isArray(error.response.data.detail)) {
        return error.response.data.detail.map((e: any) => e.msg).join(', ');
      }
      return error.response.data.detail;
    }
    return error?.message || 'Error desconocido';
  };

  const handleInputChange = (field: keyof RequestFormData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.value;
    setFormData(prev => ({
      ...prev,
      [field]: field === 'company_id' || field === 'purpose' 
               ? value 
               : parseFloat(value) || 0
    }));
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      console.log('handleSubmit - formData.company_id:', formData.company_id);
      console.log('handleSubmit - companies:', companies);
      console.log('handleSubmit - current company:', company);
      
      // Obtener la empresa según el company_id del formulario
      let targetCompany = company;
      if (!targetCompany && formData.company_id) {
        // Intentar buscar por ID numérico
        const numericId = parseInt(formData.company_id);
        targetCompany = companies.find(c => c.id === numericId) || null;
        
        // Si no se encuentra, intentar búsqueda por string
        if (!targetCompany) {
          targetCompany = companies.find(c => String(c.id) === formData.company_id) || null;
        }
        
        console.log('Search results:', { 
          numericId, 
          stringId: formData.company_id,
          foundCompany: targetCompany 
        });
      }

      if (!targetCompany) {
        console.error('No company found - formData.company_id:', formData.company_id);
        console.error('Available companies:', companies.map(c => ({ id: c.id, name: c.name })));
        setError('Debe seleccionar una empresa válida');
        return;
      }

      if (editingRequest) {
        await RequestService.updateRequestFromForm(parseInt(editingRequest.id), formData, targetCompany);
      } else {
        await RequestService.createRequestFromForm(formData, targetCompany);
      }
      
      setOpen(false);
      setEditingRequest(null);
      resetForm();
      loadRequests();
    } catch (error) {
      console.error('Error submitting request:', error);
      setError(parseErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      company_id: companyId || '',
      amount: 0,
      purpose: '',
      credit_score: 0,
      debt_to_equity_ratio: 0,
      years_in_business: 0,
      cash_flow: 0
    });
  };

  const handleEdit = (request: RiskRequest) => {
    setEditingRequest(request);
    setFormData({
      company_id: request.company_id,
      amount: request.amount,
      purpose: request.purpose,
      credit_score: request.risk_inputs.credit_score,
      debt_to_equity_ratio: request.risk_inputs.debt_to_equity_ratio,
      years_in_business: request.risk_inputs.years_in_business,
      cash_flow: request.risk_inputs.cash_flow
    });
    setOpen(true);
  };

  const handleDeleteClick = (request: RiskRequest) => {
    setRequestToDelete(request);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!requestToDelete) return;

    try {
      setLoading(true);
      await RequestService.deleteRequest(parseInt(requestToDelete.id));
      setDeleteDialogOpen(false);
      setRequestToDelete(null);
      loadRequests();
    } catch (error) {
      console.error('Error deleting request:', error);
      setError(parseErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const handleDialogClose = () => {
    setOpen(false);
    setEditingRequest(null);
    resetForm();
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

  const getCompanyName = (companyId: string) => {
    console.log('getCompanyName called with:', { companyId, companies, companiesLength: companies.length });
    
    // Intentar encontrar por ID como número (tipo original)
    const numericId = parseInt(companyId);
    let foundCompany = companies.find(c => c.id === numericId);
    
    // Si no se encuentra, intentar como string
    if (!foundCompany) {
      foundCompany = companies.find(c => String(c.id) === companyId);
    }
    
    console.log('Search results:', { 
      numericId, 
      foundByNumber: companies.find(c => c.id === numericId),
      foundByString: companies.find(c => String(c.id) === companyId),
      finalFound: foundCompany,
      companyIds: companies.map(c => ({ id: c.id, type: typeof c.id, name: c.name }))
    });
    
    return foundCompany ? foundCompany.name : `Empresa ID: ${companyId}`;
  };

  if (loading && !company && requests.length === 0) {
    return (
      <Container 
        maxWidth="lg" 
        sx={{ 
          mt: 4, 
          display: 'flex', 
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '60vh',
          flexDirection: 'column',
          gap: 2
        }}
      >
        <LoadingSpinner variant="dots" size="large" />
        <Typography 
          variant="h6" 
          color="text.secondary"
          sx={{ 
            opacity: 0.7,
            textAlign: 'center',
            fontWeight: 400,
            background: 'linear-gradient(45deg, #2563eb 30%, #10b981 90%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          Cargando evaluaciones de riesgo...
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header con estilos mejorados */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Box>
          <Button
            startIcon={<ArrowBack />}
            onClick={() => navigate(companyId ? '/companies' : '/dashboard')}
            sx={{ 
              mb: 2,
              '&:hover': {
                transform: 'translateX(-4px)',
                transition: 'transform 0.2s ease-in-out'
              }
            }}
            className="hover-lift"
          >
            {companyId ? 'Volver a Empresas' : 'Volver al Dashboard'}
          </Button>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
            <TrendingUp sx={{ fontSize: 40, color: 'primary.main' }} />
            <Typography 
              variant="h4" 
              component="h1" 
              sx={{ 
                fontWeight: 700,
                background: 'linear-gradient(45deg, #2563eb 30%, #10b981 90%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              {companyId ? 'Evaluaciones de Riesgo' : 'Todas las Evaluaciones de Riesgo'}
            </Typography>
          </Box>
          
          {company && (
            <Card sx={{ 
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              mb: 2,
              borderRadius: 3,
              maxWidth: 400
            }}>
              <CardContent sx={{ py: 2 }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  {company.name}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  {company.industry} • {company.company_size ? `${company.company_size} empleados` : 'Tamaño no especificado'}
                </Typography>
              </CardContent>
            </Card>
          )}
          
          {!companyId && (
            <Typography 
              variant="h6" 
              color="text.secondary" 
              sx={{ 
                opacity: 0.8,
                fontWeight: 400 
              }}
            >
              Vista general de todas las evaluaciones
            </Typography>
          )}
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Tabla de evaluaciones con estilos mejorados */}
      <Card 
        sx={{ 
          mb: 3,
          borderRadius: 3,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
          background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
          border: '1px solid rgba(37, 99, 235, 0.1)',
          '&:hover': {
            boxShadow: '0 12px 40px rgba(0, 0, 0, 0.15)',
            transform: 'translateY(-2px)',
          },
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
        }}
        className="hover-lift"
      >
        <CardContent sx={{ p: 0 }}>
          <Box 
            sx={{ 
              p: 3, 
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white'
            }}
          >
            <Typography 
              variant="h6" 
              sx={{ 
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: 2
              }}
            >
              <Assessment sx={{ fontSize: 28 }} />
              Historial de Evaluaciones
            </Typography>
            <Typography 
              variant="body2" 
              sx={{ 
                opacity: 0.9, 
                mt: 0.5 
              }}
            >
              {requests.length} evaluación{requests.length !== 1 ? 'es' : ''} registrada{requests.length !== 1 ? 's' : ''}
            </Typography>
          </Box>
          
          <TableContainer 
            component={Paper} 
            sx={{ 
              borderRadius: 0,
              boxShadow: 'none'
            }}
          >
            <Table>
              <TableHead>
                <TableRow 
                  sx={{
                    background: 'linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%)',
                    '& th': {
                      fontWeight: 600,
                      color: '#1e293b',
                      fontSize: '0.875rem',
                      borderBottom: '2px solid #e2e8f0',
                      py: 2
                    }
                  }}
                >
                  <TableCell>📅 Fecha</TableCell>
                  {!companyId && <TableCell>🏢 Empresa</TableCell>}
                  <TableCell>💰 Monto (USD)</TableCell>
                  <TableCell>📝 Propósito</TableCell>
                  <TableCell>⭐ Puntuación de Riesgo</TableCell>
                  <TableCell>🎯 Nivel de Riesgo</TableCell>
                  <TableCell>✅ Aprobado</TableCell>
                  <TableCell>⚙️ Acciones</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {/* Solo mostrar evaluaciones si:
                    1. Es vista específica (companyId existe), O
                    2. Es vista general Y las empresas están cargadas */}
                {(companyId || (!companyId && companies.length > 0)) && requests.map((request) => (
                  <TableRow 
                    key={request.id}
                    sx={{
                      '&:hover': {
                        backgroundColor: 'rgba(37, 99, 235, 0.04)',
                        transform: 'scale(1.001)',
                        transition: 'all 0.2s ease-in-out'
                      },
                      '&:nth-of-type(even)': {
                        backgroundColor: 'rgba(248, 250, 252, 0.5)'
                      },
                      cursor: 'pointer'
                    }}
                    className="table-row-hover"
                  >
                    <TableCell>
                      {new Date(request.created_at).toLocaleDateString('es-ES')}
                    </TableCell>
                    {!companyId && (
                      <TableCell>
                        <Typography variant="body2">
                          {getCompanyName(request.company_id)}
                        </Typography>
                      </TableCell>
                    )}
                    <TableCell>${request.amount.toLocaleString()}</TableCell>
                    <TableCell>{request.purpose}</TableCell>
                    <TableCell>
                      <Box 
                        sx={{ 
                          display: 'flex', 
                          alignItems: 'center', 
                          gap: 1 
                        }}
                      >
                        <Box
                          sx={{
                            width: 40,
                            height: 40,
                            borderRadius: '50%',
                            background: `conic-gradient(
                              ${request.risk_score <= 30 ? '#10b981' : 
                                request.risk_score <= 70 ? '#f59e0b' : '#ef4444'} 
                              ${request.risk_score * 3.6}deg, 
                              #e5e7eb 0deg
                            )`,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: 'white',
                            fontWeight: 'bold',
                            fontSize: '0.75rem',
                            boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                          }}
                        >
                          {request.risk_score}
                        </Box>
                        <Typography 
                          variant="body2" 
                          color="text.secondary"
                          sx={{ fontSize: '0.75rem' }}
                        >
                          /100
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={request.risk_level}
                        color={getRiskLevelColor(request.risk_level) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={request.approved ? 'SÍ' : 'NO'}
                        color={request.approved ? 'success' : 'error'}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        <Tooltip title="Editar">
                          <IconButton
                            onClick={() => handleEdit(request)}
                            size="small"
                            sx={{
                              backgroundColor: 'rgba(37, 99, 235, 0.1)',
                              color: '#2563eb',
                              '&:hover': {
                                backgroundColor: 'rgba(37, 99, 235, 0.2)',
                                transform: 'scale(1.1)',
                              },
                              transition: 'all 0.2s ease-in-out'
                            }}
                          >
                            <Edit fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Eliminar">
                          <IconButton
                            onClick={() => handleDeleteClick(request)}
                            size="small"
                            sx={{
                              backgroundColor: 'rgba(239, 68, 68, 0.1)',
                              color: '#ef4444',
                              '&:hover': {
                                backgroundColor: 'rgba(239, 68, 68, 0.2)',
                                transform: 'scale(1.1)',
                              },
                              transition: 'all 0.2s ease-in-out'
                            }}
                          >
                            <Delete fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
                
                {/* Mensaje cuando no hay empresas cargadas en vista general */}
                {!companyId && companies.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={8} sx={{ textAlign: 'center', py: 4 }}>
                      <Typography variant="body2" color="text.secondary">
                        Cargando información de empresas...
                      </Typography>
                    </TableCell>
                  </TableRow>
                )}
                
                {/* Mensaje cuando no hay evaluaciones (solo si tenemos empresas o es vista específica) */}
                {((companyId || (!companyId && companies.length > 0)) && requests.length === 0) && (
                  <TableRow>
                    <TableCell colSpan={companyId ? 7 : 8} align="center" sx={{ py: 6 }}>
                      <Box 
                        sx={{ 
                          display: 'flex', 
                          flexDirection: 'column', 
                          alignItems: 'center',
                          gap: 2,
                          py: 4
                        }}
                      >
                        <Assessment 
                          sx={{ 
                            fontSize: 64, 
                            color: 'text.disabled',
                            opacity: 0.3
                          }} 
                        />
                        <Typography 
                          variant="h6" 
                          color="text.secondary"
                          sx={{ fontWeight: 400 }}
                        >
                          No hay evaluaciones de riesgo registradas
                        </Typography>
                        <Typography 
                          variant="body2" 
                          color="text.disabled"
                        >
                          Haz clic en el botón "+" para crear tu primera evaluación
                        </Typography>
                      </Box>
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Botón flotante para nueva evaluación mejorado */}
      <Fab
        color="primary"
        aria-label="add"
        sx={{ 
          position: 'fixed', 
          bottom: 24, 
          right: 24,
          background: 'linear-gradient(45deg, #2563eb 30%, #10b981 90%)',
          boxShadow: '0 8px 32px rgba(37, 99, 235, 0.3)',
          width: 64,
          height: 64,
          '&:hover': {
            background: 'linear-gradient(45deg, #1d4ed8 30%, #059669 90%)',
            transform: 'scale(1.1)',
            boxShadow: '0 12px 40px rgba(37, 99, 235, 0.4)',
          },
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:active': {
            transform: 'scale(0.95)',
          }
        }}
        onClick={() => setOpen(true)}
        className="floating-action-button"
      >
        <Add sx={{ fontSize: 32 }} />
      </Fab>

      {/* Dialog para crear/editar evaluación */}
      <Dialog open={open} onClose={handleDialogClose} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingRequest ? 'Editar Evaluación de Riesgo' : 'Nueva Evaluación de Riesgo'}
        </DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            {/* Información de la empresa (solo lectura) */}
            {company && (
              <Box sx={{ mb: 3, p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
                <Typography variant="h6" gutterBottom>
                  Datos de la Empresa (automáticos)
                </Typography>
                <Box sx={{ display: 'flex', gap: 2, mb: 1 }}>
                  <Typography variant="body2">
                    <strong>Ingresos Anuales:</strong> ${company.annual_revenue.toLocaleString()} USD
                  </Typography>
                  <Typography variant="body2">
                    <strong>Empleados:</strong> {company.company_size}
                  </Typography>
                </Box>
                <Typography variant="body2">
                  <strong>Industria:</strong> {company.industry}
                </Typography>
              </Box>
            )}
            
            {/* Formulario de evaluación */}
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {/* Selector de empresa (solo en vista general) */}
              {!companyId && (
                <TextField
                  select
                  label="Seleccionar Empresa"
                  fullWidth
                  value={formData.company_id}
                  onChange={handleInputChange('company_id')}
                  required
                  SelectProps={{
                    native: true,
                  }}
                >
                  <option value="">Seleccione una empresa</option>
                  {companies.map((comp) => (
                    <option key={comp.id} value={comp.id}>
                      {comp.name} - {comp.industry}
                    </option>
                  ))}
                </TextField>
              )}
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  label="Monto del Préstamo (USD)"
                  type="number"
                  fullWidth
                  value={formData.amount}
                  onChange={handleInputChange('amount')}
                  required
                  inputProps={{ min: 0 }}
                  helperText="Cantidad solicitada en dólares"
                />
                <TextField
                  label="Propósito del Préstamo"
                  fullWidth
                  value={formData.purpose}
                  onChange={handleInputChange('purpose')}
                  required
                  helperText="Ej: expansión, inventario, equipos"
                />
              </Box>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  label="Años en el Negocio"
                  type="number"
                  fullWidth
                  value={formData.years_in_business}
                  onChange={handleInputChange('years_in_business')}
                  required
                  inputProps={{ min: 0 }}
                  helperText="Tiempo de operación de la empresa"
                />
                <TextField
                  label="Puntuación de Crédito (FICO)"
                  type="number"
                  fullWidth
                  value={formData.credit_score}
                  onChange={handleInputChange('credit_score')}
                  required
                  inputProps={{ min: 300, max: 850 }}
                  helperText="Rango: 300-850 (mayor es mejor)"
                />
              </Box>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  label="Ratio Deuda/Patrimonio"
                  type="number"
                  fullWidth
                  value={formData.debt_to_equity_ratio}
                  onChange={handleInputChange('debt_to_equity_ratio')}
                  required
                  inputProps={{ min: 0, step: 0.01 }}
                  helperText="Ejemplo: 0.5 = 50% deuda vs patrimonio"
                />
                <TextField
                  label="Flujo de Caja Anual (USD)"
                  type="number"
                  fullWidth
                  value={formData.cash_flow}
                  onChange={handleInputChange('cash_flow')}
                  required
                  helperText="Flujo de caja promedio anual"
                />
              </Box>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleDialogClose}>
              Cancelar
            </Button>
            <Button 
              type="submit" 
              variant="contained" 
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : (editingRequest ? 'Actualizar' : 'Crear')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Dialog de confirmación de eliminación */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Confirmar Eliminación</DialogTitle>
        <DialogContent>
          <Typography>
            ¿Está seguro de que desea eliminar esta evaluación de riesgo?
          </Typography>
          {requestToDelete && (
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Monto: ${requestToDelete.amount.toLocaleString()} - {requestToDelete.purpose}
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>
            Cancelar
          </Button>
          <Button 
            onClick={handleDeleteConfirm} 
            color="error" 
            variant="contained"
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Eliminar'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default RiskAssessment;
