/**
 * @typedef {Object} Article
 * @property {number} id
 * @property {string} title
 * @property {string|null} content
 * @property {string|null} summary
 * @property {string} source
 * @property {string} url
 * @property {number|null} cluster_id
 * @property {string|null} published_at
 * @property {string} created_at
 */

/**
 * @typedef {Object} Cluster
 * @property {number} id
 * @property {string} title
 * @property {string|null} summary
 * @property {string} created_at
 */

/**
 * @typedef {Object} ClusterDetail
 * @property {number} id
 * @property {string} title
 * @property {string|null} summary
 * @property {string} created_at
 * @property {Article[]} articles
 */

/**
 * @typedef {Object} SourceReference
 * @property {string} title
 * @property {string} source
 * @property {string} url
 */

/**
 * @typedef {Object} ChatResponse
 * @property {string} conversation_id
 * @property {string} answer
 * @property {SourceReference[]} sources
 */