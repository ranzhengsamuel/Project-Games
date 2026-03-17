# Docker Findings

## Image Sizes
- my-stub (python:3.11-slim): 52MB
- my-stub-alpine (python:3.11-alpine): 26.9MB

## Why they differ
Alpine Linux strips out all unnecessary system tools and libraries,
keeping only the bare minimum, which makes it much smaller than the slim image. 
