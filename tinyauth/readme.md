# tinyauth

> A tiny passwordless authentication service

This template "saasifies" an example REST API [httbin.org](https://httpbin.org). It uses a standard [OpenAPI](https://swagger.io/specification/) spec to describe the API's endpoints.

Saasify acts as a proxy in front of this external API to handle auth, billing, rate limiting, etc. This allows your backend API to focus solely on your product's unique value proposition.

Once you're ready, you'll want to replace this OpenAPI spec with one representing your externally hosted API.

_Note that an OpenAPI spec is no longer required to use Saasify_. Including an OpenAPI spec allows Saasify to auto-generate API docs for your product. It also allows Saasify to perform additional validation as it proxies HTTP calls to your backend API.

See our [quick start](https://docs.saasify.sh/#/quick-start) for a walkthrough of how to get started and our [OpenAPI guide](https://docs.saasify.sh/#/openapi) for more information on generating your own OpenAPI spec.

## License

_This project was bootstrapped with [Saasify](https://saasify.sh)._

MIT © [jottenlips](https://github.com/jottenlips)
