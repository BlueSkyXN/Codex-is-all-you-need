---
name: dev-build-optimization
description: Use for diagnosing or improving build speed, bundle size, cache behavior, monorepo task execution, packaging output, and reproducible builds.
---

# Build optimization workflow

Use this workflow when a build, bundle, compile, package, or monorepo task is slow, unstable, or too large.

## Steps

1. Identify the build surface.
   - Package manager, workspace layout, build tool, bundler, compiler, CI job, cache configuration, and output artifact.

2. Establish a baseline.
   - Cold build time
   - Incremental build time
   - Bundle or artifact size
   - Cache hit/miss evidence
   - Relevant CI logs

3. Find bottlenecks.
   - Dependency graph
   - Type checking
   - Transpilation
   - Minification
   - Asset handling
   - Test execution
   - Remote/cache setup

4. Apply targeted improvements.
   - Incremental compilation
   - Parallel tasks
   - Cache configuration
   - Tree shaking
   - Code splitting
   - Dependency dedupe
   - Build script simplification

5. Validate before and after.
   - Run comparable commands.
   - Confirm output still works.
   - Check source maps, assets, and package contents when relevant.

## Output

Return:

1. Baseline
2. Bottleneck evidence
3. Change summary
4. Before/after validation
5. Remaining build risk

## Do not

- Do not claim improvement without comparable measurements.
- Do not remove checks from builds just to make them faster.
- Do not change package output semantics without calling out compatibility impact.
