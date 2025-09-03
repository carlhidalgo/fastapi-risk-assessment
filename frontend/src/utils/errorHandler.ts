export const parseErrorMessage = (error: any): string => {
  if (error.response?.data) {
    const errorData = error.response.data;
    
    // Handle validation errors (array of error objects)
    if (Array.isArray(errorData.detail)) {
      return errorData.detail
        .map((err: any) => err.msg || err.message || 'Validation error')
        .join(', ');
    } 
    // Handle simple string errors
    else if (typeof errorData.detail === 'string') {
      return errorData.detail;
    }
    // Handle general error objects
    else if (errorData.message) {
      return errorData.message;
    }
  }
  
  // Fallback error message
  return error.message || 'An unexpected error occurred';
};
