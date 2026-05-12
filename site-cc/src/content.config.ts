import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const pages = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/pages' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    order: z.number().default(99),
  }),
});

const book = defineCollection({
  loader: glob({
    pattern: ['**/*.md', '!**/00-design.md'],
    base: '../books',
  }),
  schema: z.object({
    kind: z.enum(['book', 'part', 'section']),
    book: z.string().optional(),
    slug: z.string(),
    title: z.string(),
    subtitle: z.string().optional(),
    part: z.string().optional(),
    order: z.number().default(99),
    status: z.enum(['draft', 'published']).default('draft'),
    summary: z.string().optional(),
    author: z.string().optional(),
    licence: z.string().optional(),
    licenceUrl: z.string().url().optional(),
    description: z.string().optional(),
    keywords: z.array(z.string()).optional(),
  }),
});

export const collections = { pages, book };
