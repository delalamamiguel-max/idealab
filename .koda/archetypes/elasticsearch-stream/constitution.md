
# ElasticSearch Stream Archetype Constitution

## Purpose
Establish standard, secure, and efficient practices for Python scripts, applications, or Jupyter notebooks that read, transform, or write to ElasticSearch indices via EventHub topics.

## I. Hard-Stop Rules (Non-Negotiable)
- ✘ Every ElasticSearch query MUST include a filter, match, or term condition.
- ✘ Credentials (any kind) MUST be read from Azure KeyVault.
- ✘ Python library installation or upgrade commands MUST NOT be present in the codebase.
- ✘ DBFS usage in Databricks notebooks is prohibited.
- ✘ EventHub payloads MUST include: `env`, `feed`, `aiopxServiceId`, `escollection`, `yyyymmdd`.

## II. Mandatory Patterns (Must Apply)
- ✔ ElasticSearch scroll contexts MUST specify a size.
- ✔ EventHub batch payloads MUST NOT exceed 1 MB.
- ✔ Unity Catalog MUST be used for configuration storage and retrieval.
- ✔ Exception handling MUST use user-defined class types.
- ✔ Code MUST be optimized with explicit exit conditions for compute efficiency.

## III. Preferred Patterns (Recommended)
- ➜ Parameterize common configurable variables.
- ➜ Typecast all attributes in payloads written to ElasticSearch indices.

## IV. Example: EventHub Payload Construction

```python
def build_eventhub_payload(env, feed, aiopxServiceId, escollection, yyyymmdd, data):
	return {
		"env": env,
		"feed": feed,
		"aiopxServiceId": aiopxServiceId,
		"escollection": escollection,
		"yyyymmdd": yyyymmdd,
		"data": data
	}
```

## V. Version
- 1.0.0

## VI. Last Updated
- 2025-10-24
