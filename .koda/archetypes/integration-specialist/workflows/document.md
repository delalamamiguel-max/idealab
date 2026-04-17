---
description: Generate documentation for REST/GraphQL APIs (Integration Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype integration-specialist --json ` and parse for API_FRAMEWORK, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/integration-specialist/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: API spec or code, target audience (developers, integrators), documentation scope (API reference, integration guide, user guide). Request clarification if incomplete.

### 4. Analyze Code/System

Analyze API: identify all endpoints and operations, document request/response schemas, explain authentication and authorization, note rate limiting and quotas, identify error codes and handling, document webhooks and callbacks.

### 5. Generate Documentation

Create comprehensive documentation with: API overview and getting started, authentication guide, endpoint reference (all methods, parameters, responses), code examples in multiple languages, error handling guide, rate limiting documentation, changelog and versioning.

Include OpenAPI/Swagger spec, Postman collection, integration guide, SDK documentation.

### 6. Add Recommendations

Include recommendations for documentation maintenance (versioning, deprecation notices), API best practices, security considerations, monitoring and analytics, client library usage.

### 7. Validate and Report


Generate documentation artifacts. Report completion.

## Error Handling

**Insufficient Context**: Request complete API spec or code.

**Missing Examples**: Generate code examples for common use cases.

**Unclear Authentication**: Request authentication flow details.

## Examples

**Example 1**: `/document-api Create docs for orders API` - Output: API reference with endpoints, schemas, examples

**Example 2**: `/document-api Generate integration guide for payment service` - Output: Integration guide with authentication, examples, error handling

**Example 3**: `/document-api Document GraphQL API for developers` - Output: GraphQL docs with queries, mutations, schema

## References

