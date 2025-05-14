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
* **Storage medium compromised**: It must be assumed that an adversary has full access to the device and its stored data. The security of the system must rely exclusively on secrets not stored on the device itself.

In the following, I outline a system architecture designed to meet the specified criteria. My aim with this paper was to design and articulate a coherent model grounded in practical and adversarial threat assumptions. The design emerged from a playful exploration of cryptographic techniques and is intended as an intellectual exercise rather than a proposal for a deployable real-world system. At the time of writing, I am a master's student in mathematics.

*Note: The language in this document has been polished with the assistance of ChatGPT to improve clarity and formality.*

## Cryptographic Primitives
The system assumes the availability of the following secure primitives:

* Symmetric Encryption $\mathbb{E}_K[\mathrm{data}]$: A CPA-secure, preferably authenticated encryption scheme (e.g., AES-GCM, XChaCha20-Poly1305).

* Hash Function $\mathrm{hash}$: A collision-resistant function used for integrity, lookup obfuscation, and key derivation.

* Key Derivation Function $\mathrm{KDF}(p,\mathrm{salt})$: A memory-hard function (e.g., Argon2) that derives high-entropy keys from low-entropy secrets.

* Random Number Generator $\mathrm{random}()$: A cryptographically secure generator for keys, salts, and nonces.

## How the System Works for Users

The system enables users to create custom directory hierarchies with robust, dual-mode access control. For illustration, consider the following example structure created by Alice. Some folders are marked with `*` or `!``, which we will explain shortly:

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
├── *📁 Sources
│   ├── 📁 Interviews
│   │   ├── 📄 Interview_with_Activist_1.mp3
│   │   └── 📄 Interview_with_Political_Dissident_2.docx
│   ├── *📁 Whistleblower_Reports
│   │   ├── 📄 Report_on_Government_Corruption_1.pdf
│   │   └── 📄 Report_on_Forced_Disappearances.pdf
│   └── *📁 Evidence
│       ├── 📄 Surveillance_Logs.pdf
│       └── 📄 Leaked_Emails_Chain.pdf
├── !📁 Sources
│   ├── 📁 Interviews
│   │   ├── 📄 Interview_with_Local_Teacher.mp3
│   │   └── 📄 Interview_with_Street_Vendor.docx
│   ├── 📁 Notes
│   │   ├── 📄 Market_Economy_Notes.txt
│   │   └── 📄 Regional_Culture_Observations.txt
│   └── 📁 Media_Tips
│       ├── 📄 How_to_Use_VPNs_Safely.pdf
│       └── 📄 Beginner_Guide_to_OSINT.pdf
├── *📁 Media
│   ├── 📁 Photos
│   │   ├── 📷 Protest_Images.jpeg
│   │   └── 📷 Interview_Photos.jpeg
│   └── 📁 Videos
│       ├── 🔈 Interview_Clip.mp4
│       └── 🔈 Protest_Footage.mp4
```
Each folder in the system supports two access modes: primary and duress. Within a directory there exist a set of subfolders and files that are said to be shared, allowing read and write operations by both modes. Additionaly, however, each mode posses their own hidden subdirectories, inaccassible to the other mode. In the example above, folders marked with `*` are visible only in the primary mode, and those marked with `!` are visible only in the duress mode.

Access modes are recursively enforced: once a directory is accessed in a given mode, all its descendants are automatically interpreted in the same mode. This prevents mode escalation and ensures mode isolation within any given subtree.

Each folder may be protected with two passwords: a primary password and a duress password. Entering a password grants access to the folder in the corresponding mode. Crucially, passwords work independently of the parent folder's state, meaning a user can unlock and access a deeply nested folder directly, even if its ancestors remain locked or hidden. This decoupling allows granular sharing of specific folders without revealing the broader structure.

Moreover, the system is designed to prevent metadata leakage. The existence of folders that have not been unlocked remains undiscoverable, protecting against both inference attacks and accidental disclosure under coercion.

### Example Scenarios
1. #### Accessing the Root with the Primary Password
Reveals all shared content and the primary-only directories:

```
📁 Root
├── 📁 Articles
│   ├── 📁 Published
│   └── 📁 Drafts
│   └── 📁 Research
├── *📁 Sources
│   ├── 📁 Interviews
│   ├── *📁 Whistleblower_Reports
│   └── *📁 Evidence
├── *📁 Media
│   ├── 📁 Photos
│   └── 📁 Videos
```

2. #### Accessing the Root with the Duress Password
Displays shared content and the duress-only directories:

```
📁 Root
├── 📁 Articles
│   ├── 📁 Published
│   └── 📁 Drafts
│   └── 📁 Research
├── !📁 Sources
│   ├── 📁 Interviews
│   ├── 📁 Notes
│   └── 📁 Media_Tips
```

3. #### Accessing a Specific Folder Directly
For instance, entering the primary password for the *Sources* folder (without unlocking *Root*) reveals only the primary-mode content of that folder and its subdirectories:

```
📁 Sources
├── 📁 Interviews
├── *📁 Whistleblower_Reports
└── *📁 Evidence
```
This model allows Alice to selectively share specific folders (such as *Sources*) with collaborators, using a designated password, without revealing the rest of her directory structure or inadvertently granting access to sensitive materials stored elsewhere.

Clarifying Remarks
* *Absence of Credential Mapping Metadata*: The system stores no mappings between passwords and folders, in plaintext or encrypted form. Folder access is derived solely through decryption, and without a valid password, no structural or identifying information is revealed. Encrypted data appears indistinguishable from random noise.

* *Undetectability of Duress Passwords*: The system cannot distinguish between primary and duress credentials. All password-derived keys are treated equally, and hidden folders under duress access appear identical to regular ones. There are no markers or flags; the `*` and `!` prefix is purely illustrative our examples.

* *Structural Obfuscation as a Security Goal*: The system prevents inference of folder structure even under full storage compromise. Without decryption keys, no information about a folder's position—root, intermediate, or leaf—is revealed. The system ensures asymmetric visibility: users may enumerate contents below any folder they can decrypt, but not above.

The technical mechanisms used to enforce these guarantees—such as key derivation, encrypted index resolution, and forward-secure path construction—are detailed in the next sections.
