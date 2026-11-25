export const LANGS = ['en', 'ru', 'zh-cn', 'es', 'de'] as const;
export type Lang = (typeof LANGS)[number];

export interface LangMeta {
  label: string;
  htmlLang: string;
  title: string;
  description: string;
  keywords: string;
}

export const META: Record<Lang, LangMeta> = {
  en: {
    label: 'English',
    htmlLang: 'en',
    title: 'Universal AI Capability Platform — Provider-neutral AI capability registry',
    description: 'Provider-neutral registry, evaluator, router and execution runtime for Hugging Face, MCP, OpenAPI and A2A. Immutable contracts, policy gates, knowledge graph and LLM-ready wiki.',
    keywords: 'AI capability registry, AI router, MCP tools, Hugging Face, A2A agents, knowledge graph, LLM wiki',
  },
  ru: {
    label: 'Русский',
    htmlLang: 'ru',
    title: 'Универсальная платформа AI-возможностей — реестр и роутер',
    description: 'Провайдер-нейтральный реестр, оценщик, роутер и runtime для HF, MCP, OpenAPI и A2A. Неизменяемые контракты, политика, knowledge graph и вики для LLM.',
    keywords: 'реестр AI-возможностей, AI роутер, MCP инструменты, Hugging Face, A2A агенты, граф знаний, вики для LLM',
  },
  'zh-cn': {
    label: '简体中文',
    htmlLang: 'zh-CN',
    title: '通用 AI 能力平台 — 供应商无关的能力注册中心',
    description: '面向 Hugging Face、MCP、OpenAPI 和 A2A 的供应商无关注册中心、评估器、路由器与执行运行时。不可变契约、策略门控、知识图谱与 LLM 知识库。',
    keywords: 'AI 能力注册中心, AI 路由器, MCP 工具, Hugging Face, A2A 智能体, 知识图谱, LLM 维基',
  },
  es: {
    label: 'Español',
    htmlLang: 'es',
    title: 'Plataforma Universal de Capacidades de IA — registro de capacidades',
    description: 'Registro, evaluador, enrutador y motor de ejecución independiente del proveedor para Hugging Face, MCP, OpenAPI y A2A. Contratos inmutables y wiki para LLM.',
    keywords: 'registro de capacidades de IA, enrutador de IA, herramientas MCP, Hugging Face, agentes A2A, grafo de conocimiento',
  },
  de: {
    label: 'Deutsch',
    htmlLang: 'de',
    title: 'Universelle AI-Fähigkeitsplattform — anbieterneutrales Register',
    description: 'Anbieterneutrales Register, Bewertungssystem, Router und Ausführungsmodul für Hugging Face, MCP, OpenAPI und A2A. Unveränderliche Verträge und LLM-Wiki.',
    keywords: 'AI-Fähigkeitsregister, AI-Router, MCP-Werkzeuge, Hugging Face, A2A-Agenten, Wissensgraph, LLM-Wiki',
  },
};

export function isLang(value: string): value is Lang {
  return (LANGS as readonly string[]).includes(value);
}
