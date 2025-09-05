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
import { Add, Edit, Delete, ArrowBack } from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { CompanyService } from '../services/companyService';
import { RequestService } from '../services/requestService';
import { Company } from '../types/company';
import { RiskRequest, RequestFormData } from '../types/request';

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
      setLoading(true);
      const companyData = await CompanyService.getCompany(parseInt(companyId));
      setCompany(companyData);
    } catch (error) {
      console.error('Error loading company:', error);
      setError('Error al cargar la empresa');
    } finally {
      setLoading(false);
    }
  };

  // Cargar todas las empresas (para vista general)
  const loadCompanies = async () => {
    if (companyId) return; // Solo cargar si estamos en vista general
    
    try {
      const companiesData = await CompanyService.getCompanies();
      setCompanies(companiesData);
    } catch (error) {
      console.error('Error loading companies:', error);
    }
  };

  // Cargar evaluaciones de riesgo
  const loadRequests = async () => {
    try {
      setLoading(true);
      // Si hay companyId, filtrar por empresa específica, si no, mostrar todas
      const params = companyId ? { company_id: companyId } : {};
      const requestsData = await RequestService.getRequests(params);
      setRequests(requestsData.items);
    } catch (error) {
      console.error('Error loading requests:', error);
      setError('Error al cargar las evaluaciones de riesgo');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      await loadCompany();
      await loadCompanies();
      await loadRequests();
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
      // Obtener la empresa según el company_id del formulario
      let targetCompany = company;
      if (!targetCompany && formData.company_id) {
        targetCompany = companies.find(c => c.id === parseInt(formData.company_id)) || null;
      }

      if (!targetCompany) {
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
    const foundCompany = companies.find(c => c.id === parseInt(companyId));
    return foundCompany ? foundCompany.name : `Empresa ID: ${companyId}`;
  };

  if (loading && !company) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Box>
          <Button
            startIcon={<ArrowBack />}
            onClick={() => navigate(companyId ? '/companies' : '/dashboard')}
            sx={{ mb: 2 }}
          >
            {companyId ? 'Volver a Empresas' : 'Volver al Dashboard'}
          </Button>
          <Typography variant="h4" component="h1" gutterBottom>
            {companyId ? 'Evaluaciones de Riesgo' : 'Todas las Evaluaciones de Riesgo'}
          </Typography>
          {company && (
            <Typography variant="h6" color="text.secondary">
              {company.name} - {company.industry}
            </Typography>
          )}
          {!companyId && (
            <Typography variant="h6" color="text.secondary">
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

      {/* Tabla de evaluaciones */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Historial de Evaluaciones
          </Typography>
          
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Fecha</TableCell>
                  {!companyId && <TableCell>Empresa</TableCell>}
                  <TableCell>Monto (USD)</TableCell>
                  <TableCell>Propósito</TableCell>
                  <TableCell>Puntuación de Riesgo</TableCell>
                  <TableCell>Nivel de Riesgo</TableCell>
                  <TableCell>Aprobado</TableCell>
                  <TableCell>Acciones</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {requests.map((request) => (
                  <TableRow key={request.id}>
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
                      <Typography variant="h6">
                        {request.risk_score}/100
                      </Typography>
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
                      <Tooltip title="Editar">
                        <IconButton
                          onClick={() => handleEdit(request)}
                          size="small"
                        >
                          <Edit />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Eliminar">
                        <IconButton
                          onClick={() => handleDeleteClick(request)}
                          size="small"
                          color="error"
                        >
                          <Delete />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
                {requests.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={companyId ? 7 : 8} align="center">
                      <Typography variant="body2" color="text.secondary">
                        No hay evaluaciones de riesgo registradas
                      </Typography>
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Botón flotante para nueva evaluación */}
      <Fab
        color="primary"
        aria-label="add"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        onClick={() => setOpen(true)}
      >
        <Add />
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
                />
                <TextField
                  label="Propósito del Préstamo"
                  fullWidth
                  value={formData.purpose}
                  onChange={handleInputChange('purpose')}
                  required
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
                />
                <TextField
                  label="Puntuación de Crédito"
                  type="number"
                  fullWidth
                  value={formData.credit_score}
                  onChange={handleInputChange('credit_score')}
                  required
                  inputProps={{ min: 300, max: 850 }}
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
                />
                <TextField
                  label="Flujo de Caja (USD)"
                  type="number"
                  fullWidth
                  value={formData.cash_flow}
                  onChange={handleInputChange('cash_flow')}
                  required
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
