# Sedryx Hycrypta

*Encrypted file manager • Duress passwords • Direct folder access with no structural leaks*

---

## Abstract
In this README, I present a cryptographically secure file-management design that assumes an adversary with full access to all stored data. My goal is to describe a coherent model grounded in realistic threat assumptions. This work is an intellectual exercise—emerging from my own exploration of cryptographic techniques—and is not a ready-for-production proposal.

I’m currently a mathematics master’s student with no formal cryptography training, so I welcome any feedback or corrections. If any of these ideas mirror existing research, I assure you it was unintentional—I deliberately avoided surveying the literature until after drafting this design. My only “collaborator” was ChatGPT for polishing the prose.

## Motivation
Consider the case of Alice, a high-risk individual—such as a journalist operating under an authoritarian regime—who requires a secure and reliable mechanism for storing highly sensitive information. To meet her stringent security needs, she turns to her technically proficient associate, Bob, with a request to design a system that satisfies the following set of rigorous requirements:

* **Encryption**: All data stored within the system must be encrypted.

* **Metadata obfuscation**: Directory hierarchies, file names, access patterns, and all related metadata must be effectively concealed.

* **Password-derived keys**: Access to encrypted data must rely exclusively on keys derived from user-provided passwords. Without knowledge uniquely held by Alice, it should be cryptographically infeasible to extract any information from the storage medium.

* **Alternative credentials**: The system must support the use of alternate passwords, each granting access only to a restricted subset of the data. This enables Alice to divulge a decoy password under coercion, thereby protecting more sensitive information.

* **Plausible deniability**: The system must ensure that alternative credentials are indistinguishable from one another—both to an external adversary and to the system itself—thus preserving deniability about the existence of hidden data.

* **Folder-level access control**: The system should allow individual folders to be protected by their own passwords, enabling direct access to specific folders without requiring traversal of the entire directory structure or knowledge of the master password. This must be achieved without revealing any information about the overall structure of the file system.

## Cryptographic Primitives
The system relies on the availability of the following cryptographic primitives:

* *Symmetric Encryption*: $\mathbb{E}_K[\mathrm{data}]$
A symmetric encryption scheme, preferably with built-in authentication (e.g., AEAD). This serves as the primary mechanism for encrypting data throughout the system.

* *Asymmetric Encryption*: $\mathbf{A}_K[\mathrm{data}]$
An asymmetric encryption scheme, employed primarily to enable support for dual-access credentials and secure key distribution.

* *Hash Function*: $\mathrm{hash}(\mathrm{data}, \mathrm{salt})$
A collision-resistant hash function, used for purposes such as ensuring data integrity, obfuscating lookup structures, and contributing to key derivation.

* *Key Derivation Function*: $\mathrm{KDF}(\mathrm{password}, \mathrm{salt})$
A memory-hard key derivation function—such as Argon2—used to transform low-entropy secrets (e.g., user passwords) into high-entropy cryptographic keys.

* *Cryptographically Secure Random Number Generator*: $\mathrm{random}(n)$
A secure source of randomness for generating cryptographic materials including keys, salts, and nonces.

## How the System Works for Users
The system allows users to construct custom directory hierarchies with strong, dual-mode access control. To illustrate its functionality, consider the following example hierarchy created by Alice. Some folders are annotated with `*` or `!`, which will be explained shortly:

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
Each folder supports two access modes: primary and duress. Subfolders and files within a directory may be either:

* **Shared**: accessible in both modes,

* **Primary-only**: accessible exclusively in primary mode (`*`),

* **Duress-only**: accessible exclusively in duress mode (`!`).

Access modes are recursively enforced. Once a folder is opened in a particular mode, all its descendants are interpreted under the same mode. This prevents escalation or leakage between modes and guarantees complete isolation of access contexts.

Each folder can be protected by two independent passwords: a primary password and a duress password. Entering either grants access in the corresponding mode. Crucially, access is non-hierarchical—a folder can be unlocked directly without requiring decryption or knowledge of its parent directories. This decoupled access model enables secure and granular sharing of individual subdirectories without exposing the broader structure.

Furthermore, the system is designed to eliminate metadata leakage. The existence of any folder not explicitly unlocked remains completely undiscoverable. Neither adversaries nor coerced users can infer the presence of hidden content.

### Example Scenarios
1. #### Accessing the Root with the Primary Password
Reveals shared content and primary-mode folders:

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
Reveals shared content and duress-mode folders:

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

3. #### Direct Access to a Specific Folder
Entering the primary password for the *Sources* folder—without unlocking the root—reveals only the primary content of that folder:

```
📁 Sources
├── 📁 Interviews
├── *📁 Whistleblower_Reports
└── *📁 Evidence
```
This enables users like Alice to securely share individual folders (e.g., *Sources*) with collaborators via a designated password, without revealing unrelated or more sensitive parts of the file system.


Clarifying Remarks
* **Absence of Credential Mapping Metadata**:
The system does not store any explicit mapping between passwords and folders, whether in plaintext or encrypted form. Folder discovery is purely decryption-based: without a valid password, no structural, semantic, or identifying information is revealed. Encrypted data is indistinguishable from random bytes.

* **Undetectability of Duress Passwords**:
The system cannot distinguish between primary and duress credentials. All password-derived keys are processed uniformly. Hidden directories in duress mode appear identical to any other folder, and there are no internal indicators to suggest the presence of an alternate access mode. The * and ! annotations are merely explanatory for this example.

* **Structural Obfuscation as a Security Principle**:
Even in the event of complete storage compromise, the system discloses no information about the directory structure. Without valid decryption keys, it is impossible to infer a folder’s position in the hierarchy—whether root, intermediate, or leaf. Access is asymmetrically visible: users may traverse downward from any folder they can decrypt, but cannot infer the existence or layout of ancestor or sibling folders.

## System Overview
#### Lookup Architecture
To allow for efficient and selective lookups while preserving secrecy about the directory structure, the system employs lookup tables of the form:

$$\{\mathrm{hash}(\mathrm{key}, \mathrm{salt}): \mathbb{E}_{\mathrm{key}}[\mathrm{data}]\}$$
This should enable selective decryption while disallowing inference about inaccessible elements. Only with the correct key can one discover the presence and location of the corresponding data.

#### Folders Attributes
Each folder has the following attributes, each unique to it

* Keys
- *Primary Keys* $(p, P)$: A public–private key pair responsible for the primary access mode.
- *Duress Keys* $(d, D)$: A public–private key pair responsible for the duress access mode.
- *Shared Key* $S$: An encryption key used by both access modes to store shared metadata.
- *Data Encryption Key* $E$: Used to encrypt files inside the folder.

* Salts
- *Child Salt* $cs$: Used for lookups to locate children of the folder (i.e., subfolders).
- *File Salt* $fs$: Used for lookups to locate files directly under the folder.
- *Password Salt* $ps$: Used during password derivation; each folder has a unique value.
- *Key Salt* $ks$: Used in lookups that locate other keys (e.g., stored child keys).

#### Key Structure
The system is fundamentally built on recursive key-to-key encryption: keys are used to encrypt other keys, which in turn encrypt further keys, and so on. This is the backbone of both metadata obfuscation and strict access mode separation.

The lookup structure ensures that only valid keys can discover and decrypt the data they are authorized to access. This is also how access mode boundaries are cryptographically enforced: for example, the primary mode cannot reveal information exclusive to the duress mode and vice versa.

Suppose a user is inside a directory and wishes to create a new folder. We’ll denote the parent folder's attributes in **bold** and the child’s in regular font. When creating the folder, the user can choose to make it either:

* **Shared** (visible in both access modes), or

* **Hidden** (visible only in the current access mode).

This decision determines which keys will be used to store and later retrieve the child folder. The key hierarchy follows the structure illustrated below. Each arrow denotes that the key below can derive the key above, and edge labels show which salt is involved in the lookup.

Let:
* $P_p$: Primary password of the child folder.
* $P_d$: Duress password of the child folder.
* $K_p$, $K_d$: Keys derived from $P_p$ and $P_d$ respectively via a KDF and the salt $ps$.

[Insert proper graph graphic]
[
bold(p) ->{ks} ->
Pp ->{KDF, ps} -> Kp ->
                         S ->{ks} E
Pd ->{KDF, ps} -> Kd ->
bold{d} ->{ks} ->
]

This makes the recursive nature of access control clear. For example, the primary key of the parent folder ($\mathbf{p}$) can only derive the primary password of the child, and hence only the primary child keys. It cannot access the duress keys or any data protected solely under them — making escalation between modes cryptographically impossible.

#### Directory Storage
Folders securely maintain references to their children while attempting to minimize metadata leakage. Any element intended to be accessible in both modes is encrypted using the shared key $S$.
Each child is stored in a lookup table as an entry of the form: $$\{\mathrm{hash}(S, \mathrm{salt}): \mathbb{E}_{S}[\mathrm{child_id}]\}$$
Where $\mathrm{salt}$ is either the `child_salt` or `file_salt` depending on whether the child is a folder or file. Thus, only possession of the correct shared key allows traversal to these shared children. Private (mode-specific) children would instead be stored under the corresponding mode’s key.

#### Password Access
When the program is initialized, the user is prompted for a password. Based on the password entered, the system attempts to open the root folder associated with it — without knowing anything about the underlying directory structure or access mode.

Here is how this process works:

1. The user is prompted to enter a password $P$.

2. A global salt $s$ (randomly generated when the vault is first created) is used to derive a candidate root key: $r := \mathrm{KDF}(P, s)$.

3. A global lookup table of the form $\{\mathrm{hash}(r) : \mathbb{E}_{r}[ps]\}$ is consulted. This table is stored with the vault metadata and allows the system to discover root folders corresponding to different passwords without revealing the folder structure.

4. If a match is found, the program uses $r$ to decrypt the entry and obtain $ps$, the password salt for the folder.

5. The true folder key is then derived as $K := \mathrm{KDF}(P, ps)$, which may be either a primary or duress key — the system cannot tell.

6. The folder and all of its descendants may now be accessed using $K$.

## Implementation
### Storage Backend
While the system is designed to remain agnostic to the underlying storage mechanism, a relational database such as SQLite is particularly well-suited for this application due to its simplicity, efficiency, and widespread availability. The schema below defines how the system persists encrypted folder metadata, file data, and access-control lookup entries. All cryptographic operations are performed externally to the database, which stores only encrypted or hashed values.

Two separate SQLite databases are required: one primary database that stores all persistent operational data, and a secondary database used during initialization to manage user password prompts and authentication. Both databases are permanent and persist data across sessions, but they serve distinct functions within the system.

#### Database Schema
##### `folder` Table
| Column          | Type    | Description                                                             |
| --------------- | ------- | ----------------------------------------------------------------------- |
| `id`            | INTEGER | Unique identifier for the folder                                        |
| `name`          | BLOB    | Encrypted folder name using the shared key $S$                          |
| `password_salt` | BLOB    | Encrypted password salt using $S$                                       |
| `file_salt`     | BLOB    | Encrypted salt for file lookups using $S$                               |
| `child_salt`    | BLOB    | Encrypted salt for child lookups using $S$                              |
| `key_salt`      | BLOB    | Public salt used in key lookups (unencrypted)                           |
| `key1`          | BLOB    | Public key for either the primary or duress mode (unencrypted)          |
| `key2`          | BLOB    | Public key for the complementary mode (duress or primary) (unencrypted) |

*Note: Whether `key1` is primary or duress is not recorded explicitly. The distinction is only meaningful once the corresponding private key is derived from a password.*

##### `file` Table
| Column      | Type    | Description                                           |
| ----------- | ------- | ------------------------------------------------------|
| `id`        | INTEGER | Unique identifier for the file                        |
| `name`      | BLOB    | Encrypted file name using the data encryption key $E$ |
| `extension` | BLOB    | Encrypted file extension using $E$                    |
| `contents`  | BLOB    | Encrypted file contents using $E$                     |


##### `key_lookup` Table
| Column | Type | Description                                       |
| ------ | ---- | ------------------------------------------------- |
| `hash` | BLOB | Hashed key used for lookup                        |
| `key`  | BLOB | Encrypted key blob                                |


##### `child_lookup` Table
| Column     | Type | Description                          |
| ---------- | ---- | -------------------------------------|
| `hash`     | BLOB | Hashed index for child folder lookup |
| `child_id` | BLOB | Encrypted folder ID                  |

##### `file_lookup` Table
| Column    | Type | Description                  |
| --------- | ---- | -----------------------------|
| `hash`    | BLOB | Hashed index for file lookup |
| `file_id` | BLOB | Encrypted file ID using $S$  |

### Folder Creation
To implement the key-chaining mechanism described earlier, the following table entries are added when a new folder is created. Let $\mathbf{k}$ denote either $\mathbf{p}$ (primary), $\mathbf{d}$ (duress), or $\mathbf{S}$ (shared key), depending on the parent's current access mode and the visibility configuration of the new folder.

1. `folder`
| `id` | `name`  | `password_salt` | `file_salt` | `child_salt` | `key1` | `key2` |
| ---- | ----------- | --------------- | ----------- | ------------ | ------ | ------ |
| ...  | $\mathbb{E}_S[\mathrm{folder_name}]$ | $ps$          | $fs$      | $cs$       | $p$  | $d$  |


2. `child_lookup`
| `hash`                                     | `child_id`     |
| ------------------------------------------ | -------------- |
| $\mathrm{hash}(\mathbf{k}, \mathbf{cs})$ | (encrypted ID) |

3. `key_lookup`
| `hash`                            | `key`                            |
| --------------------------------- | -------------------------------- |
| $\mathrm{hash}(p, ks)$          | $\mathbb{E}_p[S]$            |
| $\mathrm{hash}(d, ks)$          | $\mathbb{E}_d[S]$            |
| $\mathrm{hash}(S, ks)$          | $\mathbb{E}_S[E]$            |
| $\mathrm{hash}(\mathbf{p}, ks)$ | $\mathbb{E}_{\mathbf{p}}[p]$ |
| $\mathrm{hash}(\mathbf{d}, ks)$ | $\mathbb{E}_{\mathbf{d}}[d]$ |

## Initialization Database
To securely manage user authentication and facilitate folder access without prior knowledge of the directory structure, the system employs a dedicated initialization database. This database persists essential metadata and a lookup table to verify passwords and retrieve corresponding folder salts during startup.

### Database Schema
1. `meta` Table
| Column  | Type | Description                                               |
| ------- | ---- | --------------------------------------------------------- |
| `key`   | TEXT | Identifier for the metadata entry (e.g., `global_salt`) |
| `value` | BLOB | Corresponding data stored unencrypted (e.g., `global salt`) |

* Stores critical global parameters such as the public global salt $s$ used in key derivation.

2. `password_lookup` Table

| Column          | Type | Description                                                |
| --------------- | ---- | ---------------------------------------------------------- |
| `hash`          | BLOB | Hash of the derived key `r := KDF(password, s)`            |
| `password_salt` | BLOB | Encrypted folder-specific password salt `\mathbb{E}_r[ps]` |

* Maps the hash of the key derived from the user’s input password combined with the global salt to the encrypted folder-specific password salt.

* Enables the system to verify password correctness and derive further keys without exposing directory structure details.

## Potential Applications
### Denaiable Messaging
The system could underpin a secure messaging platform where each message is stored as a file in a root folder. Both communicating devices would be provisioned with the primary and duress credentials. Messages exchanged under duress are stored as normal files, while more sensitive messages can be encrypted under the primary key. If coerced, users can reveal only the duress password, leaving no cryptographic evidence of a second conversation. Additional cover traffic and randomized padding can be employed to obscure the existence of hidden data entirely.

### Secure Colloboration
This configuration emphasizes access control rather than strict secrecy. Suppose two users, Eve and Olivia, collaborate on a shared project using a third-party cloud service. By configuring the server with this system, each user can maintain private encrypted folders and share selected folders with their counterpart. Access is managed entirely through cryptography; the server itself never knows which folders are shared or private, nor does it need to enforce permissions. All access control is client-driven and cryptographically guaranteed.
