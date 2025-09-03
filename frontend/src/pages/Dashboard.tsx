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
  TextField,
  Button,
  Box,
  Chip,
  IconButton
} from '@mui/material';
import { Add, Visibility, Edit } from '@mui/icons-material';
import { requestsApi, companiesApi } from '../services/api';

interface Request {
  id: string;
  company_id: string;
  amount: number;
  purpose: string;
  risk_score: number;
  status: string;
  created_at: string;
}

interface Company {
  id: string;
  name: string;
  industry: string;
  size: string;
}

const Dashboard: React.FC = () => {
  const [requests, setRequests] = useState<Request[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [requestsResponse, companiesResponse] = await Promise.all([
        requestsApi.getAll(1, search),
        companiesApi.getAll(1)
      ]);
      
      setRequests(requestsResponse.items || []);
      setCompanies(companiesResponse.items || []);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCompanyName = (companyId: string) => {
    const company = companies.find(c => c.id === companyId);
    return company ? company.name : 'Unknown';
  };

  const getRiskColor = (score: number) => {
    if (score <= 50) return 'success';
    if (score <= 75) return 'warning';
    return 'error';
  };

  const getRiskLabel = (score: number) => {
    if (score <= 50) return 'Low Risk';
    if (score <= 75) return 'Medium Risk';
    return 'High Risk';
  };

  if (loading) {
    return (
      <Container>
        <Typography>Loading...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Risk Assessment Dashboard
        </Typography>
        <Button variant="contained" startIcon={<Add />}>
          New Request
        </Button>
      </Box>

      <Box mb={3}>
        <TextField
          fullWidth
          placeholder="Search companies..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && loadData()}
        />
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Company</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Purpose</TableCell>
              <TableCell>Risk Score</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {requests.map((request) => (
              <TableRow key={request.id}>
                <TableCell>{getCompanyName(request.company_id)}</TableCell>
                <TableCell>${request.amount.toLocaleString()}</TableCell>
                <TableCell>{request.purpose}</TableCell>
                <TableCell>
                  <Chip
                    label={`${request.risk_score} - ${getRiskLabel(request.risk_score)}`}
                    color={getRiskColor(request.risk_score) as any}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={request.status}
                    variant="outlined"
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <IconButton size="small">
                    <Visibility />
                  </IconButton>
                  <IconButton size="small">
                    <Edit />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {requests.length === 0 && (
        <Box textAlign="center" mt={4}>
          <Typography variant="body1" color="text.secondary">
            No requests found. Create your first risk assessment request.
          </Typography>
        </Box>
      )}
    </Container>
  );
};

export default Dashboard;
