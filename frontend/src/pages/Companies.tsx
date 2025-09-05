import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Alert,
  IconButton,
  Tooltip,
  Skeleton
} from '@mui/material';
import { Add, Edit, Delete, Assessment } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { CompanyService } from '../services/companyService';
import { Company, CompanyFormData } from '../types/company';
import { parseErrorMessage } from '../utils/errorHandler';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

const Companies: React.FC = () => {
  const navigate = useNavigate();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [open, setOpen] = useState(false);
  const [editingCompany, setEditingCompany] = useState<Company | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [companyToDelete, setCompanyToDelete] = useState<Company | null>(null);
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<CompanyFormData>({
    name: '',
    email: '',
    phone: '',
    industry: '',
    annual_revenue: 0,
    company_size: 0
  });

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      setLoading(true);
      setError(null);
      const companiesData = await CompanyService.getCompanies();
      setCompanies(companiesData);
    } catch (error) {
      console.error('Error loading companies:', error);
      setError(parseErrorMessage(error));
    } finally {
      setLoading(false);
      setInitialLoading(false);
    }
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError(null);
      
      if (editingCompany) {
        await CompanyService.updateCompany(Number(editingCompany.id), formData);
      } else {
        await CompanyService.createCompany(formData);
      }
      
      setOpen(false);
      setEditingCompany(null);
      resetForm();
      await loadCompanies();
    } catch (error) {
      console.error('Error saving company:', error);
      setError(parseErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      email: '',
      phone: '',
      industry: '',
      annual_revenue: 0,
      company_size: 0
    });
  };

  const handleEdit = (company: Company) => {
    setEditingCompany(company);
    setFormData({
      name: company.name,
      email: company.email,
      phone: company.phone,
      industry: company.industry,
      annual_revenue: company.annual_revenue,
      company_size: company.company_size
    });
    setOpen(true);
  };

  const handleDeleteClick = (company: Company) => {
    setCompanyToDelete(company);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!companyToDelete) return;
    
    try {
      setLoading(true);
      setError(null);
      await CompanyService.deleteCompany(Number(companyToDelete.id));
      setDeleteDialogOpen(false);
      setCompanyToDelete(null);
      await loadCompanies();
    } catch (error) {
      console.error('Error deleting company:', error);
      setError(parseErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const handleRiskAssessment = (company: Company) => {
    navigate(`/companies/${company.id}/risk-assessment`);
  };

  const handleDialogClose = () => {
    setOpen(false);
    setEditingCompany(null);
    resetForm();
  };

  const handleInputChange = (field: keyof CompanyFormData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.value;
    setFormData(prev => ({
      ...prev,
      [field]: field === 'annual_revenue' || field === 'company_size' ? Number(value) : value
    }));
  };

  // Componente para mostrar skeleton de filas
  const SkeletonRow = () => (
    <TableRow>
      <TableCell><Skeleton variant="text" width={120} /></TableCell>
      <TableCell><Skeleton variant="text" width={150} /></TableCell>
      <TableCell><Skeleton variant="text" width={100} /></TableCell>
      <TableCell><Skeleton variant="text" width={100} /></TableCell>
      <TableCell><Skeleton variant="text" width={80} /></TableCell>
      <TableCell><Skeleton variant="text" width={100} /></TableCell>
      <TableCell>
        <Box display="flex" gap={1}>
          <Skeleton variant="circular" width={32} height={32} />
          <Skeleton variant="circular" width={32} height={32} />
          <Skeleton variant="circular" width={32} height={32} />
        </Box>
      </TableCell>
    </TableRow>
  );

  // Si está cargando por primera vez, mostrar spinner completo
  if (initialLoading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h4" component="h1">
            Empresas
          </Typography>
          <Skeleton variant="rectangular" width={170} height={36} sx={{ borderRadius: 1 }} />
        </Box>
        <LoadingSpinner 
          size="large" 
          message="Cargando empresas..." 
          variant="dots"
          color="primary"
        />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Empresas
        </Typography>
        <Button 
          variant="contained" 
          startIcon={<Add />} 
          onClick={() => setOpen(true)}
          disabled={loading}
        >
          Agregar Empresa
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nombre</TableCell>
              <TableCell>Correo</TableCell>
              <TableCell>Industria</TableCell>
              <TableCell>Ingresos</TableCell>
              <TableCell>Tamaño</TableCell>
              <TableCell>Creado</TableCell>
              <TableCell>Acciones</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading && !initialLoading ? (
              // Mostrar skeleton rows mientras recarga
              <>
                {[...Array(3)].map((_, index) => (
                  <SkeletonRow key={`skeleton-${index}`} />
                ))}
              </>
            ) : companies.length === 0 ? (
              // Mensaje cuando no hay empresas
              <TableRow>
                <TableCell colSpan={7} align="center" sx={{ py: 4 }}>
                  <Typography variant="body1" color="text.secondary">
                    No hay empresas registradas. ¡Agrega la primera empresa!
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              // Mostrar empresas normalmente
              companies.map((company) => (
                <TableRow key={company.id}>
                  <TableCell>{company.name}</TableCell>
                  <TableCell>{company.email}</TableCell>
                  <TableCell>{company.industry}</TableCell>
                  <TableCell>${company.annual_revenue.toLocaleString()} USD</TableCell>
                  <TableCell>{company.company_size} employees</TableCell>
                  <TableCell>{new Date(company.created_at).toLocaleDateString()}</TableCell>
                  <TableCell>
                    <Tooltip title="Evaluar Riesgo">
                      <IconButton 
                        color="primary" 
                        onClick={() => handleRiskAssessment(company)}
                        size="small"
                      >
                        <Assessment />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Editar">
                      <IconButton 
                        color="secondary" 
                        onClick={() => handleEdit(company)}
                        size="small"
                      >
                        <Edit />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Eliminar">
                      <IconButton 
                        color="error" 
                        onClick={() => handleDeleteClick(company)}
                        size="small"
                      >
                        <Delete />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={handleDialogClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingCompany ? 'Editar Empresa' : 'Agregar Nueva Empresa'}
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Nombre de la Empresa"
            value={formData.name}
            onChange={handleInputChange('name')}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Correo Electrónico"
            type="email"
            value={formData.email}
            onChange={handleInputChange('email')}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Teléfono"
            value={formData.phone}
            onChange={handleInputChange('phone')}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            select
            label="Industria"
            value={formData.industry}
            onChange={handleInputChange('industry')}
            margin="normal"
            required
          >
            <MenuItem value="Technology">Tecnología</MenuItem>
            <MenuItem value="Finance">Finanzas</MenuItem>
            <MenuItem value="Healthcare">Salud</MenuItem>
            <MenuItem value="Manufacturing">Manufactura</MenuItem>
            <MenuItem value="Retail">Comercio Minorista</MenuItem>
            <MenuItem value="Agriculture">Agricultura</MenuItem>
            <MenuItem value="Construction">Construcción</MenuItem>
            <MenuItem value="Other">Otros</MenuItem>
          </TextField>
          <TextField
            fullWidth
            label="Ingresos Anuales (USD)"
            type="number"
            value={formData.annual_revenue}
            onChange={handleInputChange('annual_revenue')}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Tamaño de la Empresa (empleados)"
            type="number"
            value={formData.company_size}
            onChange={handleInputChange('company_size')}
            margin="normal"
            required
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose} disabled={loading}>
            Cancelar
          </Button>
          <Button onClick={handleSubmit} variant="contained" disabled={loading}>
            {loading ? (editingCompany ? 'Guardando...' : 'Agregando...') : (editingCompany ? 'Guardar' : 'Agregar')}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Confirmar Eliminación</DialogTitle>
        <DialogContent>
          <Typography>
            ¿Estás seguro de que deseas eliminar la empresa "{companyToDelete?.name}"?
            Esta acción no se puede deshacer.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)} disabled={loading}>
            Cancelar
          </Button>
          <Button onClick={handleDeleteConfirm} variant="contained" color="error" disabled={loading}>
            {loading ? 'Eliminando...' : 'Eliminar'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Companies;
