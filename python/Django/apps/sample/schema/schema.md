# GraphQL Schema Documentation

## Overview

This document provides an overview of the GraphQL schema used in the `sample` application. The schema is designed to facilitate efficient and flexible data operations for both `Sample` and `Category` models. By leveraging GraphQL, clients can query and manipulate data with precision, retrieving only the necessary fields and performing complex operations in a single request.

## Purpose

The primary purpose of this schema is to:

- Enable efficient data retrieval and manipulation for the `Sample` and `Category` models.
- Provide a flexible API for clients to interact with the backend.
- Simplify the development process by offering a clear and structured way to access data.

## Key Features

### GraphQL Types

1. **CategoryType**

   - Represents the `Category` model.
   - Fields:
     - `id`: Unique identifier.
     - `name`: Name of the category.
     - `slug`: URL-friendly identifier.
     - `description`: Description of the category.
     - `created_at`: Timestamp of creation.
     - `updated_at`: Timestamp of last update.

2. **SampleType**

   - Represents the `Sample` model.
   - Fields:
     - `id`: Unique identifier.
     - `title`: Title of the sample.
     - `slug`: URL-friendly identifier.
     - `content`: Main content of the sample.
     - `excerpt`: Short summary of the sample.
     - `author`: Reference to the user who created the sample.
     - `category`: Reference to the associated category.
     - `is_published`: Publication status.
     - `published_at`: Timestamp of publication.
     - `views_count`: Number of views.
     - `likes_count`: Number of likes.
     - `created_at`: Timestamp of creation.
     - `updated_at`: Timestamp of last update.

### Queries

1. **Samples**

   - Retrieve a list of samples with optional pagination and filtering.
   - Arguments:
     - `skip`: Number of records to skip.
     - `limit`: Maximum number of records to return.
     - `published_only`: Filter for published samples.

2. **Sample**

   - Retrieve a specific sample by its ID.

3. **SampleBySlug**

   - Retrieve a specific sample by its slug.

4. **SamplesByAuthor**

   - Retrieve samples created by a specific author.
   - Arguments:
     - `author_id`: ID of the author.
     - `skip`: Number of records to skip.
     - `limit`: Maximum number of records to return.

5. **Categories**

   - Retrieve a list of all categories.

6. **Category**

   - Retrieve a specific category by its ID.

### Mutations

1. **CreateSample**

   - Create a new sample.
   - Arguments:
     - `input`: Input object containing sample details.
     - `author_id`: ID of the author.

2. **UpdateSample**

   - Update an existing sample.
   - Arguments:
     - `id`: ID of the sample to update.
     - `user_id`: ID of the user performing the update.
     - `input`: Input object containing updated sample details.
     - `is_staff`: Boolean indicating if the user is a staff member.

3. **DeleteSample**

   - Delete a sample.
   - Arguments:
     - `id`: ID of the sample to delete.
     - `user_id`: ID of the user performing the deletion.
     - `is_staff`: Boolean indicating if the user is a staff member.

## Usage

- **Developers**: Use this schema to build and test GraphQL queries and mutations for the `sample` application.
- **Clients**: Integrate this schema into your frontend applications to interact with the backend efficiently.
- **Documentation**: Refer to this document for a detailed understanding of the schema's structure and capabilities.

## Benefits

- **Efficiency**: Retrieve only the data you need, reducing payload size and improving performance.
- **Flexibility**: Combine multiple operations into a single request, simplifying client-side logic.
- **Scalability**: Easily extend the schema to support new features and models.

## Future Enhancements

- Add support for additional models and relationships.
- Implement advanced filtering and sorting capabilities.
- Enhance error handling and validation for mutations.

---

This document serves as a comprehensive guide to the GraphQL schema for the `sample` application. For further assistance, please contact the development team.