# Code Generation with Claude Dev Extension

This directory demonstrates how the Claude Dev Extension can assist with generating code based on specific requirements.

## Use Case

Generating a React component for a user registration form with validation.

## Example

Let's say we need to create a React component for a user registration form with the following requirements:

- Fields: username, email, password, confirm password
- Validation for all fields
- Display error messages for invalid inputs
- Submit button that is disabled until all fields are valid

## How Claude Dev Extension Helps

1. Understand the requirements and context (React, form validation, state management).
2. Generate the component structure and import necessary dependencies.
3. Implement form fields, state management, and validation logic.
4. Add error message display and submit button functionality.
5. Provide the complete, functional React component code.

Here's the generated code:

```jsx
import React, { useState } from 'react';

const UserRegistrationForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters long';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      // Perform registration logic here
      console.log('Form submitted:', formData);
    }
  };

  const isFormValid = Object.values(formData).every((value) => value.trim() !== '');

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          name="username"
          value={formData.username}
          onChange={handleChange}
        />
        {errors.username && <span className="error">{errors.username}</span>}
      </div>
      <div>
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>
      <div>
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
        />
        {errors.password && <span className="error">{errors.password}</span>}
      </div>
      <div>
        <label htmlFor="confirmPassword">Confirm Password:</label>
        <input
          type="password"
          id="confirmPassword"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
        />
        {errors.confirmPassword && <span className="error">{errors.confirmPassword}</span>}
      </div>
      <button type="submit" disabled={!isFormValid}>
        Register
      </button>
    </form>
  );
};

export default UserRegistrationForm;
```

## Benefits

- Rapid development: The Claude Dev Extension quickly generates a fully functional component based on the requirements.
- Best practices: The generated code follows React best practices for state management and form handling.
- Error handling: The component includes comprehensive error checking and display.
- Customization: The generated code serves as a solid starting point that can be easily customized or extended.
- Learning opportunity: Developers can learn from the generated code structure and patterns.

By using the Claude Dev Extension for code generation, developers can significantly speed up their development process and ensure that their components are built with best practices in mind from the start.