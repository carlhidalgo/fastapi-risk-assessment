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
  Alert
} from '@mui/material';
import { Add } from '@mui/icons-material';
import { CompanyService } from '../services/companyService';
import { Company, CompanyFormData } from '../types/company';
import { parseErrorMessage } from '../utils/errorHandler';

const Companies: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
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
    }
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError(null);
      await CompanyService.createCompany(formData);
      setOpen(false);
      setFormData({
        name: '',
        email: '',
        phone: '',
        industry: '',
        annual_revenue: 0,
        company_size: 0
      });
      await loadCompanies();
    } catch (error) {
      console.error('Error creating company:', error);
      setError(parseErrorMessage(error));
    } finally {
      setLoading(false);
    }
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
            </TableRow>
          </TableHead>
          <TableBody>
            {companies.map((company) => (
              <TableRow key={company.id}>
                <TableCell>{company.name}</TableCell>
                <TableCell>{company.email}</TableCell>
                <TableCell>{company.industry}</TableCell>
                <TableCell>${company.annual_revenue.toLocaleString()}</TableCell>
                <TableCell>{company.company_size} employees</TableCell>
                <TableCell>{new Date(company.created_at).toLocaleDateString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Agregar Nueva Empresa</DialogTitle>
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
            label="Ingresos Anuales"
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
          <Button onClick={() => setOpen(false)} disabled={loading}>
            Cancelar
          </Button>
          <Button onClick={handleSubmit} variant="contained" disabled={loading}>
            {loading ? 'Agregando...' : 'Agregar'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Companies;
