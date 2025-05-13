# Sedryx Hycrypta

*A secure encrypted file manager with duress passwords and a searchable, encrypted directory structure*

---

## Abstract

Consider the case of Alice, a high-risk individual—such as a journalist operating under a repressive regime—who requires a robust and trustworthy means of securely storing sensitive data. She consults her technically adept associate, Bob, with a request to design an encrypted file management system satisfying a stringent set of requirements:

* **Encryption**: All data must be encrypted.
* **No metadata leaks**: The system must prevent metadata leakage; internal directory structures, filenames, and access patterns must be encrypted or otherwise obfuscated.
* **Duress passwords**: It must support the use of duress passwords, which prevent access to select subsets of data.
* **Plausible deniability**: Real and duress credentials must be indistinguishable, both to external observers and the system itself.
* **Searchable encrypted folders**: Folder-level encryption must be supported through independent password-derived keys, enabling compartmentalized access without reliance on a single master password—facilitating collaboration or emergency data sharing.
* **Storage medium comprimsed**: It must be assumed that an adversary has full access to the device and its stored data. The security of the system must rely exclusively on secrets not stored on the device itself.

In the following, I outline a system architecture designed to meet the specified criteria. My aim with this paper was to design and articulate a coherent model grounded in practical and adversarial threat assumptions. The design emerged from a playful exploration of cryptographic techniques and is intended as an intellectual exercise rather than a proposal for a deployable real-world system. At the time of writing, I am a master's student in mathematics.

*Note: The language in this document has been polished with the assistance of ChatGPT to improve clarity and formality.*

## Cryptographic Primitives
The system assumes the availability of the following secure primitives:

* Symmetric Encryption $\mathbb{E}_K[\mathrm{data}]$: A CPA-secure, preferably authenticated encryption scheme (e.g., AES-GCM, XChaCha20-Poly1305).

* Hash Function $\mathrm{hash}$: A collision-resistant function used for integrity, lookup obfuscation, and key derivation.

* Key Derivation Function $\mathrm{KDF}(p,\mathrm{salt})$: A memory-hard function (e.g., Argon2) that derives high-entropy keys from low-entropy secrets.

* Random Number Generator $\mathrm{random}()$: A cryptographically secure generator for keys, salts, and nonces.

## How the System Works for Users
Users may create customized directory hierarchies, with optional hidden folders designated by prefixing their names with an asterisk (`*`). As an example, Alice might organize her files as follows:


```
📁 Root
├── 📁 Articles
│   ├── 📁 Published
│   │   ├── 📄 Article_1.pdf
│   │   └── 📄 Article_2.pdf
│   ├── 📁 Drafts
│   │   ├── 📄 Investigation_1.draft
│   │   └── 📄 Interview_with_Colleague.draft
│   └── 📁 Research
│       ├── 📄 Political_Sources.docx
│       └── 📄 Field_Research_Notes.pdf
├── 📁 Sources
│   ├── 📁 Interviews
│   │   ├── 📄 Interview_with_Activist_1.mp3
│   │   └── 📄 Interview_with_Political_Dissident_2.docx
│   ├── *📁 Whistleblower_Reports
│   │   ├── 📄 Report_on_Government_Corruption_1.pdf
│   │   └── 📄 Report_on_Forced_Disappearances.pdf
│   └── *📁 Evidence
│       ├── 📄 Surveillance_Logs.pdf
│       └── 📄 Leaked_Emails_Chain.pdf
├── 📁 Media
│   ├── 📁 Photos
│   │   ├── 📷 Protest_Images.jpeg
│   │   └── 📷 Interview_Photos.jpeg
│   └── 📁 Videos
│       ├── 🔈 Interview_Clip.mp4
│       └── 🔈 Protest_Footage.mp4
```
Each directory may be assigned a unique password, optionally accompanied by a duress password. Upon launching the system, the user is prompted to input a password. Access is granted only to the folder associated with that password and to its subdirectories.

For instance, supplying the correct password for the *Sources* folder reveals its full contents:

```
📁 Sources
├── 📁 Interviews
│   ├── 📄 Interview_with_Activist_1.mp3
│   └── 📄 Interview_with_Political_Dissident_2.docx
├── *📁 Whistleblower_Reports
│   ├── 📄 Report_on_Government_Corruption_1.pdf
│   └── 📄 Report_on_Forced_Disappearances.pdf
└── *📁 Evidence
│   ├── 📄 Surveillance_Logs.pdf
│   └── 📄 Leaked_Emails_Chain.pdf
```
However, if the duress password is entered instead, only non-hidden contents become visible. This restricted visibility is recursively enforced: any hidden subdirectory nested within a directory accessed via duress credentials will also remain inaccessible and invisible. In the above example, entering the duress password for *Sources* would yield:

```
📁 Sources
├── 📁 Interviews
│   ├── 📄 Interview_with_Activist_1.mp3
│   └── 📄 Interview_with_Political_Dissident_2.docx
```
Clarifying Remarks
* **Absence of Explicit Credential Mappings**: The system does not rely on a password-folder mapping stored in plaintext or encrypted form. Rather, access is derived cryptographically, and no information about the directory structure is available without successfully decrypting a given folder. Consequently, the raw data contains no metadata that could be used to infer folder relationships.

* **Password-to-Folder Mapping**: The system maintains no explicit record—neither in plaintext nor encrypted form—of which password corresponds to which folder. Without the correct decryption keys, the system cannot reveal anything about the existence, identity, or structure of folders.

* **Undetectability of Duress Passwords**:
The system possesses no mechanism for distinguishing between standard and duress credentials. When a duress password is supplied, any associated hidden folders remain entirely concealed—not merely through access restrictions, but through cryptographic indistinguishability. From the system’s perspective, the encrypted representations of hidden folders are indistinguishable from random data, and no metadata or structural markers betray their existence. The use of a `*` prefix in examples serves solely as a visual aid for human readers; in practice, hidden folders are represented identically to regular ones, devoid of any flags or identifiers that might reveal their special status.

* **Structural Obfuscation as a Security Goal**:
A central design principle of the system is the obfuscation of directory topology against adversaries, including those with complete access to the underlying storage medium. In the absence of valid decryption credentials, an adversary should be unable to infer the structural role of any encrypted object—whether it constitutes a root, an intermediate node, or a terminal leaf in the directory hierarchy. The system ensures asymmetric visibility: users may enumerate contents below any folder they can decrypt, but not above. This "downward-only" visibility constraint enforces structural non-disclosure by construction.

The technical mechanisms used to enforce these guarantees—such as key derivation, encrypted index resolution, and forward-secure path construction—are detailed in the next sections.

## Folders
When a folder is created we generate three keys for the folder $(r, d, e)$ where $r$ is the real key, $d$ is the duress key and $e$ is the encryption key.
### Encryption Key
As the name suggests this is the key used to encrypt all files under this folder.
