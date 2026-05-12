import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

const SITE = 'https://spiritualintelligence.cc';

export const GET: APIRoute = async () => {
  const all = await getCollection('book');
  const books = all
    .filter(e => e.data.kind === 'book')
    .sort((a, b) => a.data.order - b.data.order);

  const lines: string[] = [
    '# Spiritual Intelligence',
    '',
    '> Critical thinking and counter-intelligence for metaphysical and spiritual spaces. Books and analysis published progressively, with stable URLs for citation.',
    '',
  ];

  for (const book of books) {
    const bookSlug = book.data.slug;
    lines.push(`## ${book.data.title}`);
    if (book.data.subtitle) lines.push(`> ${book.data.subtitle}`);
    if (book.data.licenceUrl) lines.push(`> Licence: ${book.data.licence ?? 'CC-BY-4.0'} (${book.data.licenceUrl})`);
    lines.push('');

    const parts = all
      .filter(e => e.data.kind === 'part' && e.data.book === bookSlug)
      .sort((a, b) => a.data.order - b.data.order);

    for (const part of parts) {
      lines.push(`- [${part.data.title}](${SITE}/book/${bookSlug}/${part.data.slug}/): ${part.data.summary ?? ''}`);

      const sections = all
        .filter(
          e =>
            e.data.kind === 'section' &&
            e.data.book === bookSlug &&
            e.data.part === part.data.slug,
        )
        .sort((a, b) => a.data.order - b.data.order);

      for (const section of sections) {
        lines.push(
          `  - [${section.data.title}](${SITE}/book/${bookSlug}/${part.data.slug}/${section.data.slug}/): ${section.data.summary ?? ''}`,
        );
      }
    }
    lines.push('');
  }

  return new Response(lines.join('\n'), {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
