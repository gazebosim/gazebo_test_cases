import {XMLParser} from 'fast-xml-parser'
import fs from 'fs'
import {join} from 'path'
import * as ros2 from 'ros2-cache'
import {getNumber} from './utils'
import type GazeboDoc from './__types__/GazeboDoc'
import type GazeboRepoDocs from './__types__/GazeboRepoDocs'

type GzDocsRepo = {
  url: string
  org: string
  name: string
  branch: string
  releaseName: string
}

type GzWorldRepo = {
  url: string
  org: string
  name: string
  branch: string
  pathToWoldFiles: string
}

type GzTutorialRepos = {
  reposYamlUrl: string
  reposToSkip: string[]
  tutorialsDirectory: string
}

type SdfTutorialRepo = {
  url: string
  org: string
  name: string
  branch: string
  relativePathToManifest: string
  handlesToSkip: RegExp
}

type GetLinksArgs = {
  cacheDir: string
  gzDocsRepo: GzDocsRepo
  gzWorldRepo: GzWorldRepo
  gzTutorialRepos: GzTutorialRepos
  sdfTutorialRepo: SdfTutorialRepo
}

export async function getGazeboLinks({
  gzDocsRepo,
  gzWorldRepo,
  gzTutorialRepos,
  sdfTutorialRepo,
  cacheDir,
}: GetLinksArgs): Promise<{
  repoDocs: GazeboRepoDocs[]
  errorText?: string
}> {
  ros2.cache.makeCacheDir({path: cacheDir})

  const gzDoc = await getGzDocRepoLinks({
    cacheDir,
    url: gzDocsRepo.url,
    org: gzDocsRepo.org,
    name: gzDocsRepo.name,
    branch: gzDocsRepo.branch,
    releaseName: gzDocsRepo.releaseName,
  })

  const gzTutorials = await getGzTutorialLinks({
    cacheDir,
    reposYamlUrl: gzTutorialRepos.reposYamlUrl,
    reposToSkip: gzTutorialRepos.reposToSkip,
    tutorialsDirectory: gzTutorialRepos.tutorialsDirectory,
  })

  const sdfTutorial = await getSdfTutorialLinks({
    cacheDir,
    url: sdfTutorialRepo.url,
    org: sdfTutorialRepo.org,
    name: sdfTutorialRepo.name,
    branch: sdfTutorialRepo.branch,
    relativePathToManifest: sdfTutorialRepo.relativePathToManifest,
    handlesToSkip: sdfTutorialRepo.handlesToSkip,
  })

  const gzWorld = await getGzWorldLinks({
    cacheDir,
    repoUrl: gzWorldRepo.url,
    branch: gzWorldRepo.branch,
    org: gzWorldRepo.org,
    repo: gzWorldRepo.name,
    relativePath: gzWorldRepo.pathToWoldFiles,
  })

  const gzAll = [gzDoc, ...gzTutorials, gzWorld, sdfTutorial]

  let errorText: string | undefined
  if (gzAll.some((gz) => gz.errors.length > 0)) {
    errorText = '\nErrors\n======\n'
    gzAll.forEach((gz) => {
      if (gz.errors.length > 0) {
        errorText += `Errors in ${gz.org}/${gz.repo}:\n`
        gz.errors.forEach((error) => (errorText += ` * ${error}\n`))
        errorText += '\n'
      }
    })
  }
  return {
    repoDocs: gzAll,
    errorText,
  }
}

async function getGzWorldLinks({
  cacheDir,
  repoUrl,
  org,
  repo,
  branch,
  relativePath,
}: {
  cacheDir: string
  repoUrl: string
  org: string
  repo: string
  branch: string
  relativePath: string
}) {
  const gzWorlds: GazeboRepoDocs = {
    org,
    repo,
    branch,
    localPath: join(cacheDir, org, repo),
    docs: [],
    errors: [],
    extraLabels: ['sdf worlds'],
  }
  const errorMessage = await cloneRepo({
    url: repoUrl,
    destinationPath: gzWorlds.localPath,
    branch: gzWorlds.branch,
  })
  if (errorMessage) {
    gzWorlds.errors.push(errorMessage)
    return gzWorlds
  }
  const worldsPath = join(gzWorlds.localPath, relativePath)
  let files: string[] = []
  try {
    files = fs.readdirSync(worldsPath)
  } catch (_: unknown) {
    gzWorlds.errors.push(`Could not read the ${relativePath} directory`)
  }
  files.forEach((file) => {
    const filePath = join(worldsPath, file)
    if (fs.statSync(filePath).isDirectory()) {
      return
    } else if (!file.endsWith('.sdf')) {
      gzWorlds.errors.push(`Skipping '${file}' since it is not an SDF file`)
      return
    }
    const doc: GazeboDoc = {
      localPath: filePath,
      handle: file,
      sourceUrl: `https://github.com/${org}/${repo}/tree/${branch}/${relativePath}/${file}`,
    }
    gzWorlds.docs.push(doc)
  })
  return gzWorlds
}

async function getGzDocRepoLinks({
  cacheDir,
  url: repoUrl,
  releaseName,
  org,
  name: repo,
  branch,
}: GzDocsRepo & {cacheDir: string}) {
  const gzDoc: GazeboRepoDocs = {
    org,
    repo,
    branch,
    localPath: join(cacheDir, org, repo),
    docs: [],
    errors: [],
  }
  const errorMessage = await cloneRepo({
    url: repoUrl,
    destinationPath: gzDoc.localPath,
    branch: gzDoc.branch,
  })
  if (errorMessage) {
    gzDoc.errors.push(errorMessage)
    return gzDoc
  }

  const docsPath = join(gzDoc.localPath, releaseName)
  let files: string[] = []
  try {
    files = fs.readdirSync(docsPath)
  } catch (_: unknown) {
    gzDoc.errors.push(`Could not read the ${releaseName} directory`)
  }

  files.forEach((file) => {
    const filePath = join(docsPath, file)
    if (fs.statSync(filePath).isDirectory()) {
      return
    } else if (!file.endsWith('.md')) {
      gzDoc.errors.push(`Skipping '${file}' since it is not a markdown file`)
      return
    }
    const fileNoExt = file.replace('.md', '')
    const relativePath = join(releaseName, file)
    const relativePathNoExt = join(releaseName, fileNoExt)
    const liveUrl = `https://gazebosim.org/docs/${relativePathNoExt}`
    const sourceUrl = `https://github.com/${org}/${repo}/tree/${branch}/${relativePath}`
    const doc: GazeboDoc = {
      localPath: filePath,
      handle: fileNoExt,
      liveUrl,
      sourceUrl,
    }
    gzDoc.docs.push(doc)
  })

  return gzDoc
}

async function getGzTutorialLinks({
  cacheDir,
  reposYamlUrl,
  reposToSkip = [],
  tutorialsDirectory = 'tutorials',
}: GzTutorialRepos & {cacheDir: string}) {
  const reposYamlPath = join(cacheDir, 'repos.yaml')
  await ros2.cache.downloadFile({
    url: reposYamlUrl,
    path: reposYamlPath,
  })
  const repos = ros2.reposFile.getRepos(reposYamlPath).filter((repo) => {
    return !reposToSkip.includes(repo.name)
  })

  const gzRepos: GazeboRepoDocs[] = []
  for (const repo of repos) {
    const gzRepo: GazeboRepoDocs = {
      org: repo.org,
      repo: repo.name,
      branch: repo.version,
      majorVersion: getNumber(repo.version),
      localPath: join(cacheDir, repo.org, repo.name),
      docs: [],
      errors: [],
    }

    const errorMessage = await cloneRepo({
      url: repo.url,
      destinationPath: gzRepo.localPath,
      branch: gzRepo.branch,
    })
    if (errorMessage) {
      gzRepo.errors.push(errorMessage)
    }

    const gzWebsiteRef = repo.name.replace(/gz-/, '').replace(/-/, '_')
    const readmePath = join(gzRepo.localPath, 'README.md')
    if (fs.existsSync(readmePath)) {
      const readmeDoc: GazeboDoc = {
        localPath: readmePath,
        handle: 'README',
        liveUrl: `https://gazebosim.org/libs/${gzWebsiteRef}`,
        sourceUrl: `https://github.com/${gzRepo.org}/${gzRepo.repo}/blob/${gzRepo.branch}/README.md`,
      }
      gzRepo.docs.push(readmeDoc)
    }

    const localTutorialsPath = join(gzRepo.localPath, tutorialsDirectory)

    let files: string[] = []
    try {
      files = fs.readdirSync(localTutorialsPath)
    } catch (_: unknown) {
      gzRepo.errors.push('Could not read the tutorials directory')
    }
    files.forEach((file) => {
      const filePath = join(localTutorialsPath, file)
      if (fs.statSync(filePath).isDirectory()) {
        return
      } else if (!file.endsWith('.md')) {
        gzRepo.errors.push(`Skipping '${file}' since it is not a markdown file`)
        return
      }
      const relativePath = join(tutorialsDirectory, file)
      const fileText = fs.readFileSync(filePath, 'utf8')
      const match = fileText.match(
        /\\page\s*([a-zA-Z0-9-_]+)\s*([A-Za-z0-9-_+ :"]+)?/,
      )
      if (!match) {
        gzRepo.errors.push(`Skipping ${file}: Could not find a \\page handle`)
        return
      }
      const handle = match![1]
      const matchHeading = fileText.match(/#\s+([A-Za-z0-9-_+: "]+)/)
      const title = match[2] || (matchHeading && matchHeading[1]) || handle
      const liveUrl = `https://gazebosim.org/api/${gzWebsiteRef}/${gzRepo.majorVersion}/${handle}.html`
      const sourceUrl = `https://github.com/${gzRepo.org}/${gzRepo.repo}/tree/${gzRepo.branch}/${relativePath}`
      const doc: GazeboDoc = {
        localPath: filePath,
        handle: title,
        liveUrl,
        sourceUrl,
      }
      gzRepo.docs.push(doc)
    })
    gzRepos.push(gzRepo)
  }
  return gzRepos
}

type XmlElement = {
  '#text': string
}

type TutorialXml = {
  markdown: XmlElement | XmlElement[]
  '@_title'?: string
  '@_ref': string
}

async function getSdfTutorialLinks({
  cacheDir,
  url: repoUrl,
  org = 'gazebosim',
  name: repo = 'sdf_tutorials',
  branch = 'master',
  relativePathToManifest = 'manifest.xml',
  handlesToSkip = /(proposal|roadmap|usd|bindings)/,
}: {cacheDir: string} & SdfTutorialRepo) {
  const sdfDoc: GazeboRepoDocs = {
    org,
    repo: repo,
    branch,
    localPath: join(cacheDir, org, repo),
    docs: [],
    errors: [],
  }
  const errorMessage = await cloneRepo({
    url: repoUrl,
    destinationPath: sdfDoc.localPath,
    branch: sdfDoc.branch,
  })
  if (errorMessage) {
    sdfDoc.errors.push(errorMessage)
    return sdfDoc
  }
  const localPathToManifest = join(sdfDoc.localPath, relativePathToManifest)
  const manifest = fs.readFileSync(localPathToManifest, 'utf8')
  const parser = new XMLParser({ignoreAttributes: false})
  const xml = parser.parse(manifest)
  const tutorials = xml.content.tutorials.tutorial as TutorialXml[]

  for (const t of tutorials) {
    const handle = t['@_ref']
    const title = t['@_title']

    if (handlesToSkip && handlesToSkip.test(handle)) {
      sdfDoc.errors.push(`Skipping ${handle}`)
      continue
    }

    let markdown: string
    if (Array.isArray(t.markdown)) {
      markdown = t.markdown.slice(-1)[0]['#text']
    } else {
      markdown = t.markdown['#text']
    }

    const doc: GazeboDoc = {
      localPath: join(sdfDoc.localPath, markdown),
      handle: title || handle,
      sourceUrl: `${repoUrl}/blob/${branch}/${markdown}`,
      liveUrl: `http://sdformat.org/tutorials?tut=${handle}`,
    }
    sdfDoc.docs.push(doc)
  }
  return sdfDoc
}

async function cloneRepo({
  url: repoUrl,
  destinationPath,
  branch,
}: {
  url: string
  destinationPath: string
  branch: string
}) {
  try {
    const pullMessage = await ros2.cache.pullGitRepo({
      url: repoUrl,
      destinationPath,
      version: branch,
    })
    console.log(pullMessage)
  } catch (error) {
    let errorMessage = `Could not pull the repo: ${repoUrl}`
    if (error instanceof Error) {
      errorMessage += `: ${error.message}`
    }
    return errorMessage
  }
}

async function main() {
  const {errorText} = await getGazeboLinks({
    cacheDir: '.cache',
    gzDocsRepo: {
      url: 'https://github.com/gazebosim/docs',
      org: 'gazebosim',
      name: 'docs',
      branch: 'master',
      releaseName: 'garden',
    },
    gzWorldRepo: {
      url: 'https://github.com/gazebosim/gz-sim',
      org: 'gazebosim',
      name: 'gz-sim',
      branch: 'gz-sim7',
      pathToWoldFiles: 'examples/worlds',
    },
    gzTutorialRepos: {
      reposYamlUrl:
        'https://raw.githubusercontent.com/ignition-tooling/gazebodistro/master/collection-garden.yaml',
      reposToSkip: ['gz-cmake', 'sdf_tutorials'],
      tutorialsDirectory: 'tutorials',
    },
    sdfTutorialRepo: {
      url: 'https://github.com/gazebosim/sdf_tutorials',
      relativePathToManifest: 'manifest.xml',
      org: 'gazebosim',
      name: 'sdf_tutorials',
      branch: 'master',
      handlesToSkip: /(proposal|roadmap|usd|bindings)/,
    },
  })
  if (errorText) {
    console.error(errorText)
  }
}

if (typeof require !== 'undefined' && require.main === module) {
  main()
}
